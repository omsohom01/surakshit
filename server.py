from flask import Flask, request, jsonify, send_from_directory
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)

# Serve static files from the /images directory
@app.route('/images/<path:filename>')
def send_image(filename):
    return send_from_directory('images', filename)

# Route for serving the main HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Route to handle location data and convert it to an address
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude and longitude:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location.address if location else "Address not found"
        
        print(f"Received Location: Latitude = {latitude}, Longitude = {longitude}, Address = {address}")
        return jsonify({"message": f"Location received: {address}"})
    else:
        return jsonify({"error": "Missing latitude or longitude"}), 400

# Route to handle emergency alerts
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    department = data.get('department')
    
    if department:
        print(f"Alert sent to {department.capitalize()}")
        return jsonify({"message": f"Alert sent to {department.capitalize()}"})
    else:
        return jsonify({"error": "No department provided"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
