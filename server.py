from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim  # Import the Nominatim geocoder from Geopy

app = Flask(__name__)

# Create a geolocator instance
geolocator = Nominatim(user_agent="geoapiExercises")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']

    # Reverse geocoding to get the address
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = location.address if location else "Address not found"
    except Exception as e:
        address = "Error in finding address"

    # Print the address on the server
    print(f"Client's Address: {address}")

    # Return the address to the client
    return jsonify({'status': 'Location received', 'address': address})

@app.route('/send_alert', methods=['POST'])
def send_alert():
    alert_data = request.get_json()
    department = alert_data.get('department', 'Unknown')
    message = alert_data.get('message', 'No message')

    # Print the alert details
    print(f"Emergency alert received from {department} department: {message}")

    return jsonify({'status': 'Alert received', 'message': message, 'department': department})

if __name__ == '__main__':
    app.run(debug=True)
