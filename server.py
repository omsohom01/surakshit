from flask import Flask, request, jsonify, send_from_directory
import os
import logging
import requests

app = Flask(__name__)

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenCage API Key
OPENCAGE_API_KEY = '0a729828da444deba41bb4888ce3f7bc'

# Dictionary to store department alerts
alerts = {
    "ambulance": "Ambulance",
    "firefighter": "Firefighter",
    "rescue": "Rescue",
    "police": "Police"
}

# Serve the index.html file from the root directory
@app.route('/')
def index():
    try:
        return send_from_directory(os.getcwd(), 'index.html')
    except Exception as e:
        logger.exception("Error serving index.html")
        return "index.html not found", 404

# Serve images from the 'images' directory in the root
@app.route('/images/<path:filename>')
def images(filename):
    try:
        return send_from_directory(os.path.join(os.getcwd(), 'images'), filename)
    except Exception as e:
        logger.exception(f"Error serving image: {filename}")
        return "Image not found", 404

# Function to get address from coordinates using OpenCage API
def get_address_from_coordinates(latitude, longitude):
    try:
        response = requests.get(
            'https://api.opencagedata.com/geocode/v1/json',
            params={
                'q': f'{latitude},{longitude}',
                'key': OPENCAGE_API_KEY
            }
        )
        response.raise_for_status()  # Raises an error for bad HTTP responses
        response_data = response.json()
        if response_data['results']:
            return response_data['results'][0]['formatted']
        return "Address not found"
    except requests.exceptions.RequestException as e:
        logger.exception("Error retrieving address from OpenCage API")
        return "Error retrieving address"

# Receive and log the location data from the client
@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not latitude or not longitude:
            return jsonify({"status": "Invalid location data"}), 400

        # Get address from OpenCage API
        address = get_address_from_coordinates(latitude, longitude)

        logger.info(f"Location received: Latitude = {latitude}, Longitude = {longitude}, Address = {address}")
        return jsonify({"status": "Location received", "address": address})
    except Exception as e:
        logger.exception("Error processing location data")
        return jsonify({"status": "Failed to receive location"}), 500

# Receive and log the department alert
@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.json
        department = data.get('department')

        if not department or department not in alerts:
            logger.warning("Invalid department specified")
            return jsonify({"status": "Invalid department"}), 400

        logger.info(f"Alert sent to {alerts[department]}")
        return jsonify({"status": f"Alert sent to {alerts[department]}"})
    except Exception as e:
        logger.exception("Error processing alert")
        return jsonify({"status": "Failed to send alert"}), 500

# Receive and log user details and problem description
@app.route('/send_details', methods=['POST'])
def send_details():
    try:
        data = request.json
        name = data.get('name')
        details = data.get('details')
        address = data.get('address')

        if not name or not details or not address:
            logger.warning("Missing user details, problem description, or address")
            return jsonify({"status": "Invalid details"}), 400

        logger.info(f"Details received: Name = {name}, Address = {address}, Problem Details = {details}")
        return jsonify({"status": "Details received"})
    except Exception as e:
        logger.exception("Error processing user details")
        return jsonify({"status": "Failed to receive details"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
