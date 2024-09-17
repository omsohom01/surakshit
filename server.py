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

# Route to serve the index.html file directly from the main directory
@app.route('/')
def index():
    try:
        return send_from_directory(os.getcwd(), 'index.html')
    except Exception as e:
        logger.exception("Error serving index.html")
        return "index.html not found", 404

# Route to serve images from the 'images' directory
@app.route('/images/<path:filename>')
def images(filename):
    try:
        return send_from_directory(os.path.join(os.getcwd(), 'images'), filename)
    except Exception as e:
        logger.exception(f"Error serving image: {filename}")
        return "Image not found", 404

# Dictionary to store department alerts
alerts = {
    "ambulance": "Ambulance",
    "firefighter": "Firefighter",
    "rescue": "Rescue",
    "police": "Police"
}

# Function to get address from coordinates using OpenCage API
def get_address_from_coordinates(latitude, longitude):
    try:
        response = requests.get(
            f'https://api.opencagedata.com/geocode/v1/json',
            params={
                'q': f'{latitude},{longitude}',
                'key': OPENCAGE_API_KEY
            }
        )
        response_data = response.json()
        if response_data['results']:
            return response_data['results'][0]['formatted']
        return "Address not found"
    except Exception as e:
        logger.exception("Error getting address from OpenCage API")
        return "Error retrieving address"

# Route to receive and log the location from the client
@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']

        # Get address from OpenCage API
        address = get_address_from_coordinates(latitude, longitude)

        logger.info(f"Location received: Latitude = {latitude}, Longitude = {longitude}, Address = {address}")
        return jsonify({"status": "Location received", "address": address})
    except Exception as e:
        logger.exception("Error processing location data")
        return jsonify({"status": "Failed to receive location"}), 500

# Route to receive and log the department alert
@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.json
        department = data.get('department', '').lower()  # Convert to lowercase to make it case-insensitive

        if department in alerts:
            logger.info(f"Alert sent to {alerts[department]}")
            return jsonify({"status": f"Alert sent to {alerts[department]}"})
        else:
            logger.warning(f"Invalid department specified: {department}")
            return jsonify({"status": "Invalid department"}), 400
    except Exception as e:
        logger.exception("Error processing alert")
        return jsonify({"status": "Failed to send alert"}), 500

# Route to receive and log user details and problem description
@app.route('/send_details', methods=['POST'])
def send_details():
    try:
        data = request.json
        name = data['name']
        details = data['details']
        address = data['address']

        logger.info(f"Details received: Name = {name}, Address = {address}, Problem Details = {details}")
        return jsonify({"status": "Details received"})
    except Exception as e:
        logger.exception("Error processing user details")
        return jsonify({"status": "Failed to receive details"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
