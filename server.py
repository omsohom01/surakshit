from flask import Flask, request, jsonify, send_from_directory
from geopy.geocoders import OpenCage
import os

app = Flask(__name__)

# Use your OpenCage API key
geolocator = OpenCage(api_key="0a729828da444deba41bb4888ce3f7bc")

# Serve index.html from the root folder
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

# Serve images from the root 'images' folder
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# Endpoint for receiving location and returning address
@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not latitude or not longitude:
            return jsonify({"error": "Invalid location data"}), 400

        # Perform reverse geocoding
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location.address if location else "Address not found"
        return jsonify({"address": address})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
