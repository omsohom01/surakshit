from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dictionary to store department alerts
alerts = {
    "ambulance": "Ambulance",
    "firefighter": "Firefighter",
    "rescue": "Rescue",
    "police": "Police"
}

# Endpoint to handle location data
@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Log the received location
        if latitude and longitude:
            print(f"Received location: Latitude {latitude}, Longitude {longitude}")
            return jsonify({'message': f'Location received: Latitude {latitude}, Longitude {longitude}'})
        else:
            print("No location data received.")
            return jsonify({'message': 'No location data received'}), 400
    except Exception as e:
        print(f"Error processing location: {e}")
        return jsonify({'message': 'Error processing location'}), 500

# Endpoint to handle department alerts
@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        department = data.get('department')
        
        if department in alerts:
            message = f"Alert sent to {alerts[department]}"
            print(message)  # Log the alert message
            return jsonify({'message': message})
        else:
            print("Invalid department")
            return jsonify({'message': 'Invalid department'}), 400
    except Exception as e:
        print(f"Error processing alert: {e}")
        return jsonify({'message': 'Error processing alert'}), 500

if __name__ == '__main__':
    app.run(debug=True)
