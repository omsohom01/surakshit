from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Render the main page
@app.route('/')
def index():
    return render_template('index.html')

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
