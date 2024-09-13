from flask import Flask, request, jsonify, send_from_directory
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut
import os

app = Flask(__name__)

# OpenCage API key
API_KEY = "0a729828da444deba41bb4888ce3f7bc"
geolocator = OpenCage(API_KEY, timeout=5)

# Serve the index.html from the root directory
@app.route('/')
def serve_index():
    return send_from_directory(directory=app.root_path, path='index.html')

# Serve images from the root-level 'images' directory
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.root_path, 'images'), filename)

# Endpoint to receive location and process it
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is None or longitude is None:
        return jsonify({"error": "Invalid coordinates"}), 400

    try:
        # Reverse geocoding to get the location name
        location = geolocator.reverse(f"{latitude}, {longitude}")
        return jsonify({"location": location.address if location else "Location not found"}), 200
    except GeocoderTimedOut:
        return jsonify({"error": "Geocoding service timed out"}), 500

# Send alerts (assuming another POST request for alerts)
@app.route('/send_alert', methods=['POST'])
def send_alert():
    # Implement your alert system logic here
    return jsonify({"message": "Alert sent successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, send_from_directory
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut
import os

app = Flask(__name__)

# OpenCage API key
API_KEY = "0a729828da444deba41bb4888ce3f7bc"
geolocator = OpenCage(API_KEY, timeout=5)

# Serve the index.html from the root directory
@app.route('/')
def serve_index():
    return send_from_directory(directory=app.root_path, path='index.html')

# Serve images from the root-level 'images' directory
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.root_path, 'images'), filename)

# Endpoint to receive location and process it
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is None or longitude is None:
        return jsonify({"error": "Invalid coordinates"}), 400

    try:
        # Reverse geocoding to get the location name
        location = geolocator.reverse(f"{latitude}, {longitude}")
        return jsonify({"location": location.address if location else "Location not found"}), 200
    except GeocoderTimedOut:
        return jsonify({"error": "Geocoding service timed out"}), 500

# Send alerts (assuming another POST request for alerts)
@app.route('/send_alert', methods=['POST'])
def send_alert():
    # Implement your alert system logic here
    return jsonify({"message": "Alert sent successfully!"}), 200

if __name__ == "__main__":
    # Bind to the port provided by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
