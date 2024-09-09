from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Directory for serving static files
app.config['STATIC_FOLDER'] = 'images'

# Dictionary to store department alerts
alerts = {
    "ambulance": "Ambulance",
    "firefighter": "Firefighter",
    "rescue": "Rescue",
    "police": "Police"
}

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        if data is None:
            print("No data received.")
            return jsonify({'message': 'No data received'}), 400
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Print received data to console
        print(f"Received location data: Latitude={latitude}, Longitude={longitude}")
        
        if latitude is None or longitude is None:
            print("Latitude or Longitude missing.")
            return jsonify({'message': 'Latitude or Longitude missing'}), 400
        
        # Confirm receipt of location
        return jsonify({'message': 'Location received'})
    except Exception as e:
        print(f"Error processing location: {e}")
        return jsonify({'message': 'Error processing location'}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        if data is None:
            print("No data received.")
            return jsonify({'message': 'No data received'}), 400
        
        department = data.get('department')
        
        if department in alerts:
            message = f"Alert sent to {alerts[department]}"
            # Print alert message to console
            print(message)
            return jsonify({'message': message})
        else:
            print("Invalid department.")
            return jsonify({'message': 'Invalid department'}), 400
    except Exception as e:
        print(f"Error processing alert: {e}")
        return jsonify({'message': 'Error processing alert'}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
