from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store user details (simulating a database)
user_details = {
    'location': None,
    'departments': [],
    'name': '',
    'problemDetails': ''
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_location', methods=['POST'])
def send_location():
    try:
        data = request.json
        location = data['location']
        user_details['location'] = location
        
        logger.info(f"Location received: {location}")
        return jsonify({"status": "Location received"})
    except KeyError as e:
        logger.exception(f"KeyError: Missing {e} in the request data")
        return jsonify({"status": f"Failed to receive location: Missing {e}"}), 400
    except Exception as e:
        logger.exception("Error processing location")
        return jsonify({"status": "Failed to receive location"}), 500

@app.route('/choose_department', methods=['POST'])
def choose_department():
    try:
        data = request.json
        departments = data['departments']
        user_details['departments'] = departments
        
        logger.info(f"Departments chosen: {departments}")
        return jsonify({"status": "Departments received"})
    except KeyError as e:
        logger.exception(f"KeyError: Missing {e} in the request data")
        return jsonify({"status": f"Failed to receive departments: Missing {e}"}), 400
    except Exception as e:
        logger.exception("Error processing departments")
        return jsonify({"status": "Failed to receive departments"}), 500

@app.route('/send_details', methods=['POST'])
def send_details():
    try:
        data = request.json
        name = data['userName']  # Matching with the 'userName' in your form
        details = data['problemDetails']
        
        # Store the received details
        user_details['name'] = name
        user_details['problemDetails'] = details
        
        logger.info(f"Details received: Name = {name}, Problem Details = {details}")
        return jsonify({"status": "Details received"})
    except KeyError as e:
        logger.exception(f"KeyError: Missing {e} in the request data")
        return jsonify({"status": f"Failed to receive details: Missing {e}"}), 400
    except Exception as e:
        logger.exception("Error processing user details")
        return jsonify({"status": "Failed to receive details"}), 500

if __name__ == '__main__':
    app.run(debug=True)
