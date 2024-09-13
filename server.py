import os
from flask import Flask, request, jsonify
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

app = Flask(__name__)

# Your OpenCage API key
API_KEY = "0a729828da444deba41bb4888ce3f7bc"
geolocator = OpenCage(api_key=API_KEY)

@app.route('/')
def index():
    return "Welcome to Surakshit!"

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not latitude or not longitude:
            return jsonify({"error": "Invalid location data"}), 400

        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location.address if location else "Address not found"
        return jsonify({"address": address})

    except GeocoderTimedOut:
        return jsonify({"error": "Geocoding service timed out"}), 500
    except GeocoderUnavailable:
        return jsonify({"error": "Geocoding service unavailable"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        # Handle alert data here (e.g., send notification)
        return jsonify({"message": "Alert received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Bind to the port provided by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
