import threading
# from weatherapi import weatherfuncs
from websocket.flask_rest_api_app import start_api

# def main():
#    weatherfuncs.reqweather()


api_app = start_api()

# def run_flask():
#    """Runs the Flask app in a separate thread."""
#    api_app.run(host='localhost', port=5000, debug=True, use_reloader=False)
#
# Start Flask in a background thread
# flask_thread = threading.Thread(target=run_flask, daemon=True)
# flask_thread.start()


if __name__ == "__main__":
    api_app.run(host='localhost', port=5000, debug=True)
