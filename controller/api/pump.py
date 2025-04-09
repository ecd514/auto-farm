# websocket/pump.py
from flask import Blueprint, jsonify, request
from .db import get_db
# import RPi.GPIO as pin
import time

pump_bp = Blueprint('pump', __name__, url_prefix='/api/pump')

# pin.setwarnings(False)
# pin.setmode(pin.BCM)
# pin.setup(17, pin.OUT)


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
    cursor.execute(
        "UPDATE pump_status SET status = ? WHERE id = 1", (new_status,))
    db.commit()
    print(new_status)
    return jsonify({'status': new_status}), 200
