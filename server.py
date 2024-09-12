from flask import Flask, request, jsonify
from geopy.geocoders import OpenCage
import os

app = Flask(__name__)

# OpenCage API key
API_KEY = "0a729828da444deba41bb4888ce3f7bc"
geolocator = OpenCage(API_KEY)

@app.route('/')
def index():
    return "Welcome to Surakshit!"

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location[0]['formatted']
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
    app.run(debug=True)
