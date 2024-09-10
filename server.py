from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
geolocator = Nominatim(user_agent="emergency_alert_system")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Convert coordinates to an address
    location = geolocator.reverse(f"{latitude}, {longitude}", language='en')
    if location:
        address = location.address
    else:
        address = "Address not found"
    
    # Log the coordinates and resolved address
    print(f"Received coordinates: {latitude}, {longitude}")
    print(f"Resolved address: {address}")
    
    return jsonify({'message': f'Location received: {address}'})

@app.route('/send_alert', methods=['POST'])
def send_alert():
    # Handle alert sending logic here
    # For now, just log that an alert has been sent
    print("Alert sent")
    return jsonify({'message': 'Alert sent'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use the port from environment variable or default to 10000
    app.run(host='0.0.0.0', port=port)
