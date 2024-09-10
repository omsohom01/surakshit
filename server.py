from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

geolocator = Nominatim(user_agent="emergency_alert_system")

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Convert coordinates to address
    location = geolocator.reverse(f"{latitude}, {longitude}")
    address = location.address if location else "Address not found"
    
    # Log the coordinates and address
    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}")
    print(f"Address: {address}")

    return jsonify({'message': f"Location received. Address: {address}"})

@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    department = data.get('department')
    
    # Log the alert
    print(f"Alert sent to: {department}")
    
    return jsonify({'message': f"Alert sent to {department}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use the port from environment variable or default to 10000
    app.run(host='0.0.0.0', port=port)
