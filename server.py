from flask import Flask, request, jsonify, send_from_directory
from geopy.geocoders import OpenCage
import os

app = Flask(__name__)

# OpenCage API key from your provided information
API_KEY = "0a729828da444deba41bb4888ce3f7bc"
geolocator = OpenCage(API_KEY)

# Serve images from the 'images' folder
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# Endpoint to handle location data
@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        
        # Reverse geocoding using OpenCage API
        location = geolocator.reverse(f"{latitude}, {longitude}")
        
        if location:
            address = location[0]['formatted']
            return jsonify({'status': 'success', 'address': address})
        else:
            return jsonify({'status': 'fail', 'message': 'Location not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'message': 'An error occurred'}), 500

# Endpoint to handle alerts
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    department = data.get('department', 'emergency')
    
    # Return corresponding image based on the department
    if department == 'firefighter':
        return jsonify({'status': 'success', 'image_url': '/images/firefighter.jpg'})
    elif department == 'police':
        return jsonify({'status': 'success', 'image_url': '/images/police.jpg'})
    elif department == 'rescue':
        return jsonify({'status': 'success', 'image_url': '/images/rescue.jpg'})
    else:
        return jsonify({'status': 'success', 'image_url': '/images/emergency.jpg'})

# Default route
@app.route('/')
def index():
    return 'Welcome to Surakshit!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the environment port or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
