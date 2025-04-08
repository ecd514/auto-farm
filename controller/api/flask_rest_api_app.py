# websocket/flask.py
from flask import Flask, g
from .db import init_db, get_db
from .blueprints import pump_bp, weather_bp
# from .pump import pump_bp
# from .weather import weather_bp


def start_api():
    app = Flask(__name__)

    # Register API blueprints.
    app.register_blueprint(pump_bp)
    app.register_blueprint(weather_bp)

    # Ensure that the database connection is closed after each request.
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    # Initialize the database.
    init_db(app)

    return app
