from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Serve the index.html directly
@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

# Serve images from the 'images' directory
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# Dictionary to store department alerts
alerts = {
    "ambulance": "Ambulance",
    "firefighter": "Firefighter",
    "rescue": "Rescue",
    "police": "Police"
}

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Log location data to the console
        print(f"Received location: Latitude {latitude}, Longitude {longitude}")
        
        # Confirm receipt of location
        return jsonify({'message': 'Location received'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error processing location'}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        department = data.get('department')
        
        if department in alerts:
            message = f"Alert sent to {alerts[department]}"
            # Log alert message to console
            print(message)
            return jsonify({'message': message})
        else:
            return jsonify({'message': 'Invalid department'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error processing alert'}), 500

if __name__ == '__main__':
    app.run(debug=True)
