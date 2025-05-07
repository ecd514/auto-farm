from threading import Thread, Event
from queue import Queue
import time
from datetime import datetime, timedelta, timezone
from types import NoneType
from zoneinfo import ZoneInfo
import requests

try:
    from api import (
        is_database_initialized,
        reqweather,
        start_api
    )
except ModuleNotFoundError as import_error:
    print(f"Error: Unable to import API module. Please check path or verify file integrity. Exception message: \n{
          import_error}")
try:
    from hardware import (
        turnPumpOn,
        turnLightOn,
        turnPumpOff,
        turnLightOff
    )
except ModuleNotFoundError as import_error:
    print(f"Error: Unable to import hardware module. Please check path or verify file integrity. Exception message: \n{
          import_error}")
try:
    from soildata import (
        get_prometheus_data,
        get_active_sensors,
        get_sensor_average
    )
except ModuleNotFoundError as import_error:
    print(f"Error: Unable to import soildata module. Please check path or verify file integrity. Exception message: \n{
          import_error}")

HOST_NAME = r'localhost'
HOST_PORT = 5000
API_PROTOCOL = r'http'

API_URL = f'{API_PROTOCOL}://{HOST_NAME}:{HOST_PORT}'
WEATHER_URI = "/api/weather/forecast"

DEBUG_MODE = True
FLASK_RELOADER = False

SENSORS_EXPECTED = ['1', '2', '3', '4']
SENSOR_DATA_AVERAGE_DURATION = '2m'
PROMETHEUS_URL = r'http://localhost:9090'

database_tables = ['pump_status', 'weather_data']
api_app = start_api()


class data_object:
    """
    A wrapper class to help verify that the data used 
    is the latest.
    """

    def __init__(self, data):
        self.data = data
        self.last_update_from_thread = datetime.now(
            ZoneInfo("America/New_York"))
        self.data_from_thread_timeout_deadline = self.last_update_from_thread + \
            timedelta(seconds=10)
        self.used: bool = False

    def isDataValid(self):
        return self.data_from_thread_timeout_deadline > datetime.now(
            ZoneInfo("America/New_York"))

    def update(self, data):
        self.data = data
        self.last_update_from_thread = datetime.now(
            ZoneInfo("America/New_York"))
        self.data_from_thread_timeout_deadline = self.last_update_from_thread + \
            timedelta(seconds=10)
        self.used: bool = False

    def access(self):
        self.used = True
        return self.data


def runRetrieveDatabase(data_queue: Queue, stop_event: Event):
    """
    Runs a timer that checks the validity of the
    weather forecast data in the database.
    """
    while not stop_event.is_set():
        start_time = time.time()
        try:
            weather_json = requests.get(f'{API_URL}{WEATHER_URI}').json()
        except requests.ConnectionError:
            print("Error: Connection error")
            break  # Exist loop if connection fails
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            continue  # Continue on other errors unless event is set

        try:
            # Unpack arguments as: year, month, day, hour, minute, second
            stored_time = datetime(
                *list(map(int, weather_json['expiration_time'].split(','))),
                tzinfo=ZoneInfo("America/New_York"))

            current_time = (datetime.now(
                ZoneInfo("America/New_York")))

            if current_time > stored_time:
                print("Need to generate new data")
                weather_json = requests.post(f'{API_URL}{WEATHER_URI}').json()
                data_queue.put(weather_json) if not data_queue.full() else None
            else:
                data_queue.put(weather_json) if not data_queue.full() else None

        except KeyError as keyexception:
            print(f"Missing key in weather data: {str(keyexception)}")
            continue
        except requests.ConnectionError:
            print("Error: Connection error")
            break  # Exist loop if connection fails
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            continue  # Continue on other errors unless event is set

        elapsed_time = time.time() - start_time
        sleep_duration = max(60 - elapsed_time, 0)
        stop_event.wait(sleep_duration)


def runRetrieveSensor(prometheus_url: str, data_queue: Queue, stop_event: Event):
    """
    A function that spins up a thread to run in
    the background and query the prometheus database.
    """
    while not stop_event.is_set():
        start_time = time.time()

        try:
            # Get all active sensors
            sensors = get_active_sensors(prometheus_url)

            if not sensors:
                print("No active sensors found.")
                return

            # Create a dictionary for the results
            results = {}

            # Get average for each sensor
            for sensor in sensors:
                avg_moisture = get_sensor_average(sensor, prometheus_url)

                if avg_moisture is not None:
                    results[sensor] = {
                        "averages": {
                            "moisture": avg_moisture
                        }

                    }
            data_queue.put(results) if not data_queue.full() else None

        except Exception as e:
            print(f"Error: {e}")

        elapsed_time = time.time() - start_time
        sleep_duration = max(60 - elapsed_time, 0)
        stop_event.wait(sleep_duration)


def runFlask(host_name, port, debug_mode, reloader):
    """Runs the Flask app in a separate thread."""
    api_app.run(host=host_name, port=port,
                debug=debug_mode, use_reloader=reloader)


def main():
    # Initialize and check database.
    # NOTE: This will not leave the loop unless the database is accessible
    for table_being_verified in database_tables:
        while not is_database_initialized(table_being_verified):
            print("Required table {} not found".format(
                table_being_verified))
            time.sleep(5)
            print('Table {} is accessible'.format(
                table_being_verified))

    pump_status: bool = False

    weather_queue = Queue()
    sensor_queue = Queue()

    weather_data = data_object(None)
    sensor_data = data_object(None)

    thread_shutdown = Event()

    flask_thread = Thread(target=runFlask, daemon=True, args=(
        HOST_NAME, HOST_PORT, DEBUG_MODE, FLASK_RELOADER))
    flask_thread.start()

    database_retrieval_thread = Thread(
        target=runRetrieveDatabase,
        args=(weather_queue, thread_shutdown))
    database_retrieval_thread.start()
    print("Database thread is {}".format(
        "alive" if database_retrieval_thread.is_alive() else "dead"))

    sensor_retrieval_thread = Thread(
        target=runRetrieveSensor,
        args=(PROMETHEUS_URL, sensor_queue, thread_shutdown))
    sensor_retrieval_thread.start()

    # Wait for threads to initialize
    time.sleep(1)

    try:
        # Keep the script running to keep the servers alive
        while True:
            start_time = time.time()
            # Check if the flask thread is running and restart it if stopped.
            if not flask_thread.is_alive():
                flask_thread = Thread(target=runFlask, daemon=True, args=(
                    HOST_NAME, HOST_PORT, DEBUG_MODE, FLASK_RELOADER))
                flask_thread.start()

            if not database_retrieval_thread.is_alive():
                database_retrieval_thread = Thread(
                    target=runRetrieveDatabase,
                    args=(weather_queue, thread_shutdown))
                database_retrieval_thread.start()

            if not weather_queue.empty() and not weather_data.isDataValid():
                weather_data.update(weather_queue.get())
                print(weather_data.data['percentage_of_rain'])

            if not sensor_queue.empty() and not sensor_data.isDataValid():
                sensor_data.update(sensor_queue.get())
                print(sensor_data.data['0']['averages']['moisture'])

            if not weather_data.used and not sensor_data.used and not type(weather_data.data) == NoneType and not type(sensor_data.data) == NoneType:
                # if weather_data.access()['percentage_of_rain'] < 40 and sensor_data.access()['0']['averages']['moisture']
                if weather_data.access()['percentage_of_rain'] < 40 and not pump_status:
                    turnPumpOn()
                    pump_status = True

                elif sensor_data.access()['0']['averages']['moisture'] < 50 and not pump_status:
                    print('sensor set pump on')
                    turnPumpOn()
                    pump_status = True

                if sensor_data.access()['0']['averages']['moisture'] > 57 and pump_status:
                    turnPumpOff()
                    pump_status = False

            elapsed_time = time.time() - start_time
            sleep_duration = max(1 - elapsed_time, 0)
            time.sleep(sleep_duration)
    except KeyboardInterrupt:
        print("Shutting down servers...")
        thread_shutdown.set()


# Run the main function
if __name__ == "__main__":
    main()
