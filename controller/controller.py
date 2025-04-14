from threading import Thread, Event
from queue import Queue
import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import requests

from api import is_database_initialized, reqweather, start_api
# from soildata

HOST_NAME = r'localhost'
HOST_PORT = 5000
API_PROTOCOL = r'http'

API_URL = f'{API_PROTOCOL}://{HOST_NAME}:{HOST_PORT}'
WEATHER_URI = "/api/weather/forecast"

DEBUG_MODE = True
FLASK_RELOADER = False

database_tables = ['pump_status', 'weather_data']
api_app = start_api()


def run_retrieve_database(data_queue: Queue, stop_event: Event):
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
                data_queue.put(weather_data) if not data_queue.full() else None

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


def run_retrieve_retrieval(data_queue: Queue, stop_event: Event):
    pass


def run_flask(host_name, port, debug_mode, reloader):
    """Runs the Flask app in a separate thread."""
    api_app.run(host=host_name, port=port,
                debug=debug_mode, use_reloader=reloader)


if __name__ == "__main__":
    # Initialize and check database
    for table_being_verified in database_tables:
        while not is_database_initialized(table_being_verified):
            print("Required table {} not found".format(
                table_being_verified))
            time.sleep(5)
            print('Table {} is accessible'.format(
                table_being_verified))

    weather_queue = Queue()
    sensor_queue = Queue()

    thread_shutdown = Event()

    flask_thread = Thread(target=run_flask, daemon=True, args=(
        HOST_NAME, HOST_PORT, DEBUG_MODE, FLASK_RELOADER))
    flask_thread.start()

    database_retrieval_thread = Thread(
        target=run_retrieve_database,
        args=(thread_shutdown,))

    sensor_retrieval_thread = Thread(
        target=run_retrieve_sensor,
        args=(thread_shutdown,))

    time.sleep(1)

    try:
        # Keep the script running to keep the servers alive
        while True:
            # Check if the flask thread is running and restart it if stopped.
            if not flask_thread.is_alive():
                flask_thread = Thread(target=run_flask, daemon=True, args=(
                    HOST_NAME, HOST_PORT, DEBUG_MODE, FLASK_RELOADER))
                flask_thread.start()

            if not database_validation_thread.is_alive():
                database_validation_thread = Thread(
                    target=run_database_timer,
                    args=(thread_shutdown,))
                database_validation_thread.start()

            weather_json = weather_queue.get() if not weather_queue.empty() else None
            sensor_json = sensor_queue.get() if not sensor_queue.empty else None

            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down servers...")
        database_validation_shutdown.set()
