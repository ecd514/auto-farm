# websocket/weather.py
from flask import Blueprint, jsonify, request
from .db import get_db

weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')


@weather_bp.route('/forecast', methods=['GET'])
def get_status():
    """
    Retrieve the current weather forecast.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT temperature, chance_of_rain, detailed_forecast FROM weather_data WHERE id = 1")
    row = cursor.fetchone()
    if row and 'blank table' in row['detailed_forecast'].lower():
        print("Warning: Weather data is empty")
        # Return a blank json object and No Content http code
        return jsonify({}), 204
    return jsonify({'temperature': row['temperature'], 'percentage_of_rain': row['chance_of_rain'], 'detailed_forecast': row['detailed_forecast']}), 200
