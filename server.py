from flask import Flask, request, jsonify, render_template
import logging
import requests

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store department alert data
alerts = {
    'ambulance': 'Alert sent to Ambulance',
    'firefighter': 'Alert sent to Firefighter',
    'rescue': 'Alert sent to Rescue',
    'police': 'Alert sent to Police'
}

# OpenCage API key (update with your own API key)
OPENCAGE_API_KEY = '0a729828da444deba41bb4888ce3f7bc'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Validate coordinates
        if latitude is None or longitude is None:
            return jsonify({'message': 'Invalid coordinates'}), 400

        # Call OpenCage API to get address from coordinates
        url = f'https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={OPENCAGE_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            address = result['results'][0]['formatted'] if result['results'] else 'Unknown location'
            logger.info(f"Location received: {latitude}, {longitude}. Address: {address}")
            return jsonify({'message': 'Location received', 'address': address})
        else:
            logger.error(f"Error with OpenCage API: {response.status_code}")
            return jsonify({'message': 'Error fetching address'}), 500

    except Exception as e:
        logger.exception("Error processing /send_location")
        return jsonify({'message': 'Error processing location'}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json()
        departments = data.get('departments')

        # Validate department selection
        if not departments or not all(dep in alerts for dep in departments):
            logger.error(f"Invalid departments: {departments}")
            return jsonify({'message': 'Invalid department(s)'}), 400

        # Log the alert for selected departments
        logger.info(f"Alert sent to: {', '.join(departments)}")

        # Respond back to the client with a success message
        return jsonify({'message': f'Alert sent to {", ".join(departments)}'})
    except Exception as e:
        logger.exception("Error processing /send_alert")
        return jsonify({'message': 'Error processing alert'}), 500

if __name__ == '__main__':
    app.run(debug=True)
