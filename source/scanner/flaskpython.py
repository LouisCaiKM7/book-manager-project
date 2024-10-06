from flask import Flask, render_template, request, jsonify,redirect
import cv2
import numpy as np
from bookdatabase import database
from infoSender import InfoSender
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3




app = Flask(__name__)

@app.route('/')
def index():
    
    if 'user_id' in session:
        return render_template("index.html")
    return redirect('/login') # Redirect to the login page

from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash
app.secret_key = '123' 

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove the user ID from the session
    flash('You have been logged out.', 'success')  # Optional: flash message
    return redirect('/login') # No content response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = database()
        # Fetch the user from the database (you may need to adjust this)
        user = db.get_user_by_username(username)  # Implement this method in your database class
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']  # Store user ID in the session
            flash('Login successful!', 'success')
            return redirect('/')  # Redirect to your home page or another page after login
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


from werkzeug.security import generate_password_hash
import sqlite3

@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    db = database()
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data
        username = data['username']
        email = data['email']
        password = data['password']
        latitude = data['location']["latitude"]
        longitude = data['location']["longitude"]
        hashed_password = generate_password_hash(password)
        hashed_email = generate_password_hash(email)
        print(username,email,password,latitude,longitude)

        try:
            db.insert_user(username=username,
                           email_hash=hashed_email,  # Store raw email instead of hashed
                           password_hash=hashed_password,
                           location=str([latitude,longitude]))  # Ensure location is stringified
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Email already exists", 400
       
    return render_template('signup.html')


    


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

    
    isbn_detected = False

    detecter = InfoSender(img)
    results = detecter.main()  # Ensure that main() returns the necessary data
    db = database()
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
    app.run(debug=True,threaded=False)
