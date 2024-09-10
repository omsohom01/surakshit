from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Serve the index.html file directly from the main directory
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# Serve images from the "images" folder
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'images'), filename)

# Receive and print location from the client
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json  # Receive JSON data from client
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Print coordinates to the server logs
    print(f"Received coordinates: Latitude = {latitude}, Longitude = {longitude}")
    
    # Send response back to client with received location
    return jsonify({'message': 'Location received', 'latitude': latitude, 'longitude': longitude})

# Receive alert department data
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.json  # Receive JSON data from client
    department = data.get('department')
    
    # Print department selection to server logs
    print(f"Alert department received: {department}")
    
    # Send response back to client with received department
    return jsonify({'message': f'Department alert received: {department}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
