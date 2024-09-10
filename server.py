from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

geolocator = Nominatim(user_agent="geoapiExercises")

@app.route('/')
def index():
    return send_file('index.html')  # Serve index.html directly

@app.route('/images/<image_name>')
def serve_image(image_name):
    # Serve images from the images folder
    return send_file(f'images/{image_name}')

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Convert coordinates to an address
    location = geolocator.reverse(f"{latitude}, {longitude}", language='en')
    if location:
        address = location.address
    else:
        address = "Address not found"
    
    print(f"Received coordinates: {latitude}, {longitude}")
    print(f"Resolved address: {address}")
    
    return jsonify({'message': f'Location received: {address}'})

@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.json
    department = data.get('department')
    print(f"Alert received for {department} department")
    
    return jsonify({'message': f'Alert received for {department}'})

if __name__ == '__main__':
    app.run(debug=True)
