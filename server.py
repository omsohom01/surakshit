from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Render index.html from templates folder

# Endpoint to handle location submission
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude and longitude:
        # Log the received location
        print(f"Location received: Latitude={latitude}, Longitude={longitude}")
        return jsonify({'message': 'Location received successfully'}), 200
    else:
        return jsonify({'message': 'Invalid location data'}), 400

# Endpoint to handle alert submission for departments
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.get_json()
    department = data.get('department')
    
    if department:
        # Log the received alert
        print(f"Alert received for department: {department}")
        return jsonify({'message': f'Alert sent to {department.capitalize()}'}), 200
    else:
        return jsonify({'message': 'Invalid department data'}), 400

if __name__ == '__main__':
    # Bind to the port provided by Render or default to 5000 for local testing
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
