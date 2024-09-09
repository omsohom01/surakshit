from flask import Flask, send_from_directory, request
import os

app = Flask(__name__)

# Serve index.html from root folder
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# Serve images from the 'images' folder
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'images'), filename)

# Handle the send location route
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude and longitude:
        print(f"Received location: Latitude={latitude}, Longitude={longitude}")
        return "Location received successfully!", 200
    else:
        return "Location data is missing!", 400

# Handle the send alert route
@app.route('/send_alert', methods=['POST'])
def send_alert():
    data = request.json
    department = data.get('department')

    if department:
        print(f"Alert from department: {department}")
        return f"Alert received from {department}", 200
    else:
        return "Department not specified!", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
