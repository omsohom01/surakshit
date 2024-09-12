from flask import Flask, request, jsonify, send_from_directory
from geopy.geocoders import OpenCage
import os

app = Flask(__name__)

# Use your OpenCage API key
geolocator = OpenCage(api_key='0a729828da444deba41bb4888ce3f7bc')

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    try:
        # Perform reverse geocoding using OpenCage API
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location[0]['formatted']  # Get formatted address
        return jsonify({'address': address}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    alert_type = data.get('alert_type')

    # Handle the alert and notify responders based on alert type
    # You can add more logic here as needed
    return jsonify({'message': f"Alert of type '{alert_type}' received"}), 200

@app.route('/images/<path:filename>')
def send_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(debug=True)
