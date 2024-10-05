from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from bookdatabase import database
from infoSender import InfoSender

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    global latitude
    global longitude
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    print(f'Received location: {latitude}, {longitude}')
    return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame found'}), 400

    frame = request.files['frame']
    nparr = np.frombuffer(frame.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    db = database()
    isbn_detected = False

    detecter = InfoSender(img)
    results = detecter.main()  # Ensure that main() returns the necessary data

    if results:
          # Adjust based on your implementation
        isbn_detected = results[3]
        db.insert_book(
            isbn=results[0],
            title=results[1],
            author=results[2],
            publisher_id="null",  # Update as needed
            location=str([latitude, longitude])  # Use received location
        )

    if isbn_detected:
        return jsonify({'isbnDetected': True, 'isbn': results[0]})  # Send ISBN back if detected
    else:
        return jsonify({'isbnDetected': False})
    


@app.route('/scan', methods=['POST'])
def scan():
    action = request.form.get('action')
    if action == 'start_scan':
        # You can handle the scan initiation here
        print(action)
        
        return jsonify({'status': 'Scanning started'}), 200

    return jsonify({'status': 'Invalid action'}), 400

if __name__ == '__main__':
    app.run(debug=True)
