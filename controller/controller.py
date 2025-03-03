from threading import Thread
import time

from api.weather import reqweather, weather_forecast_data
from api.flask_rest_api_app import start_api
from api.db import is_database_initialized

database_tables = ['pump_status', 'weather_data']

api_app = start_api()


def run_flask():
    """Runs the Flask app in a separate thread."""
    api_app.run(host='localhost', port=5000, debug=True, use_reloader=False)


# Start Flask in a background thread
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()


if __name__ == "__main__":

    for table_being_verified in database_tables:
        while not is_database_initialized(table_being_verified):
            print("Required table {} not found".format(table_being_verified))
            time.sleep(5)
        print('Table {} is accessible'.format(table_being_verified))

    my_weather_data: weather_forecast_data = reqweather()
    print(my_weather_data.getData())
    try:
        # Keep the script running to keep the servers alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down servers...")
