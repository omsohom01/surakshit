from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='images', template_folder='.')
CORS(app)

# Route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

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
        
        # Log location data on server console
        print(f"Client coordinates: Latitude {latitude}, Longitude {longitude}")
        
        # Send confirmation back to the client
        return jsonify({'message': f"Location received: Latitude {latitude}, Longitude {longitude}"})
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
            # Print alert message to console
            print(message)
            return jsonify({'message': message})
        else:
            return jsonify({'message': 'Invalid department'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error processing alert'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
