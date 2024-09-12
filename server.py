from flask import Flask, request, jsonify, send_from_directory
import asyncio
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut
import os

app = Flask(__name__)

# OpenCage API key
API_KEY = "0a729828da444deba41bb4888ce3f7bc"
geolocator = OpenCage(API_KEY, timeout=5)  # Set a 5-second timeout for requests

# Serve the index.html directly from the root of the project
@app.route('/')
def serve_index():
    # Serve the index.html directly from the root of the repository
    return send_from_directory(directory=app.root_path, path='index.html')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
