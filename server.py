from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        print(f"Received location: Latitude {latitude}, Longitude {longitude}")
        
        return jsonify({'message': 'Location received'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error processing location'}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        department = data.get('department')
        
        alerts = {
            "ambulance": "Ambulance",
            "firefighter": "Firefighter",
            "rescue": "Rescue",
            "police": "Police"
        }

        if department in alerts:
            message = f"Alert sent to {alerts[department]}"
            print(message)
            return jsonify({'message': message})
        else:
            return jsonify({'message': 'Invalid department'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error processing alert'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
