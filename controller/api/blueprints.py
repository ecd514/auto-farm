# api/blueprints
from flask import Blueprint, jsonify, request
from .db import get_db
from .weather import reqweather, weather_forecast_data
from hardware import turnPumpOn, turnPumpOff, turnLightOn, turnLightOff

pump_bp = Blueprint('pump', __name__, url_prefix='/api/pump')
weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')


@pump_bp.route('/status', methods=['GET'])
def get_status():
    """
    Retrieve the current pump status.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT status FROM pump_status WHERE id = 1")
    row = cursor.fetchone()
    status = row['status'] if row else 'off'
    return jsonify({'status': status}), 200


@pump_bp.route('/status', methods=['POST'])
def update_status():
    """
    Update the pump status.
    Expects JSON with a 'status' field that must be either 'on' or 'off'.
    """
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Missing status value'}), 400

    new_status = data['status']
    if new_status not in ('on', 'off'):
        return jsonify({'error': 'Invalid status. Must be "on" or "off".'}),
        400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE pump_status SET status = ? WHERE id = 1", (new_status,))
        db.commit()
        if new_status == 'on':
            turnPumpOn()
        elif new_status == 'off':
            turnLightOff()
        else:
            turnLightOn()
            print("Error: unknown status")

    except Exception as PumpFailure:
        print("Error: Failed to update/activate pump.")
        db.rollback()
        turnPumpOff()

    return jsonify({'status': new_status}), 200


@weather_bp.route('/forecast', methods=['GET'])
def get_weather_forecast():
    """
    Retrieve the current weather forecast.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT temperature, chance_of_rain, detailed_forecast FROM weather_data WHERE id = 1")
    row = cursor.fetchone()
    if row and 'blank table' in row['detailed_forecast'].lower():
        try:
            print('Attempting weather data update...')
            update_query = '''
                UPDATE weather_data
                SET
                    temperature = :temperature,
                    chance_of_rain = :rain,
                    detailed_forecast = :detailed_forecast
                WHERE
                    id = 1
            '''
            temp_data = reqweather()

            # Execute update
            cursor.execute(update_query, temp_data)
            db.commit()  # Commit using connection, not cursor
            print('Update successful!')

            # Fetch the updated data
            cursor.execute(
                "SELECT temperature, chance_of_rain, detailed_forecast FROM weather_data WHERE id = 1"
            )
            row = cursor.fetchone()
        except Exception as e:
            print("Warning: Weather data is empty")
            print(e)
            # Return a blank json object and No Content http code
            return jsonify({'message': 'Warning: weather table is empty'}), 512
    return jsonify({'temperature': row['temperature'], 'percentage_of_rain': row['chance_of_rain'], 'detailed_forecast': row['detailed_forecast']}), 200
