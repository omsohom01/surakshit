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
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            logger.error("Latitude or Longitude not provided in the request.")
            return jsonify({'message': 'Latitude and Longitude are required.'}), 400

        # Get the address from coordinates
        address = get_address_from_coordinates(latitude, longitude)

        # Log the coordinates and address on the server
        logger.info(f"Received coordinates: Latitude = {latitude}, Longitude = {longitude}")
        logger.info(f"Address: {address}")

        # Respond back to the client
        return jsonify({
            'message': f"Location received: Latitude = {latitude}, Longitude = {longitude}",
            'address': address,
            'latitude': latitude,
            'longitude': longitude
        })
    except Exception as e:
        logger.exception("Error processing /send_location")
        return jsonify({'message': 'Error processing location'}), 500

# Route to receive and log alert department data
@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        department = data.get('department')

        if department not in alerts:
            logger.error(f"Invalid department: {department}")
            return jsonify({'message': 'Invalid department'}), 400

        # Log the alert department on the server
        logger.info(f"Alert department received: {department}")

        # Respond back to the client
        return jsonify({'message': f'Alert sent to {alerts[department]}'})
    except Exception as e:
        logger.exception("Error processing /send_alert")
        return jsonify({'message': 'Error processing alert'}), 500

if __name__ == '__main__':
    # Run the app on host 0.0.0.0 to make it accessible externally, and set port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
