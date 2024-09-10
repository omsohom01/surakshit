from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Serve index.html directly
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# Serve images from the images directory
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'images'), filename)

# Receive and log the location from the client
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json  # Receiving JSON data from the client
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Print to the server logs (Render or locally)
    print(f"Received coordinates: Latitude = {latitude}, Longitude = {longitude}")
    
    # Respond back to the client with the location data
    return jsonify({
        'message': 'Location received',
        'latitude': latitude,
        'longitude': longitude
    })

# Receive and log alert department data
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.json  # Receiving JSON data from the client
    department = data.get('department')
    
    # Print the alert info to the server logs (Render or locally)
    print(f"Alert department received: {department}")
    
    # Respond back to the client with the department data
    return jsonify({'message': f'Department alert received: {department}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
