from flask import Flask, request, jsonify
import asyncio
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

# OpenCage API key
API_KEY = "0a729828da444deba41bb4888ce3f7bc"
geolocator = OpenCage(API_KEY, timeout=5)  # Set a 5-second timeout for requests

@app.route('/')
def index():
    return "Welcome to Surakshit!"

# Async function to fetch location data
async def get_location(latitude, longitude):
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location[0]['formatted']
        return address
    except GeocoderTimedOut:
        return "Geocoding request timed out. Please try again."
    except Exception as e:
        return str(e)

@app.route('/send_location', methods=['POST'])
async def send_location():
    try:
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']

        # Call the async function to fetch the location
        address = await get_location(latitude, longitude)
        return jsonify({"message": "Location received", "address": address}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.json
        department = data['department']
        return jsonify({"message": f"Alert sent to {department} department!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set the port here
