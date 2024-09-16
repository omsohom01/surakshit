from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Dummy data for demonstration
department_images = {
    "ambulance": "images/ambulance.jpg",
    "firefighter": "images/firefighter.jpg",
    "rescue": "images/rescue.jpg",
    "police": "images/police.jpg"
}

logging.basicConfig(level=logging.INFO)

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if latitude is None or longitude is None:
            return jsonify({"error": "Invalid location data"}), 400
        
        # Assume we use OpenCage API to get the address from latitude and longitude
        address = f"Sample Address for Latitude: {latitude}, Longitude: {longitude}"

        return jsonify({"address": address}), 200
    except Exception as e:
        logging.error("Error sending location", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.json
        departments = data.get('departments', [])
        if not departments:
            return jsonify({"error": "No departments selected"}), 400

        # Process alert, for example send it to selected departments
        logging.info(f"Alert sent to: {', '.join(departments)}")

        return jsonify({"message": "Alert sent"}), 200
    except Exception as e:
        logging.error("Error sending alert", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/send_details', methods=['POST'])
def send_details():
    try:
        data = request.json
        name = data.get('name')  # Use .get() to avoid KeyError
        details = data.get('details')
        address = data.get('address')

        if not name or not details:
            return jsonify({"error": "Name and details are required"}), 400

        # Process the details here (e.g., store in a database or send an email)
        logging.info(f"Details received from {name}: {details} at {address}")

        return jsonify({"message": "Details received"}), 200
    except Exception as e:
        logging.error("Error processing user details", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
