from threading import Thread
import time

# from weatherapi import weatherfuncs
from websocket.flask_rest_api_app import start_api
from websocket.db import is_database_initialized

# def main():


api_app = start_api()


def run_flask():
    """Runs the Flask app in a separate thread."""
    api_app.run(host='localhost', port=5000, debug=True, use_reloader=False)


# Start Flask in a background thread
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()


if __name__ == "__main__":
    while not is_database_initialized('pump_status'):
        print("Pump database not initialized yet")
        time.sleep(5)
    print('Pump database accessible')
    while True:
        #        print("Main controller is running other operations...")
        time.sleep(5)  # Simulate ongoing operations
