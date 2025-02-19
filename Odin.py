# Odin.py
# The main Rust server
# By David Burke


#########################################################################################
# Import required functions
from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from Thor import taskDAO
import pandas as pd

# Initalising Database



#########################################################################################
# Initialize the Flask application
app = Flask(__name__)
# Set the secret key for session management
# This key is used to sign session cookies for security
app.secret_key = 'verySecure' 

#########################################################################################
#Passwords here
#Passwords here
#Passwords here
# A simple in-memory user store
# I would put this is a seperate paswords file in a real depoyment and this would not be uploaded to git hub for security
users = {
    "admin": generate_password_hash("password123"),  # User 1
    "andrew": generate_password_hash("streachYourLegs"), # User 2
    "david": generate_password_hash("myMumHasLitACandle") # User 3
}

#########################################################################################
#########################################################################################
#########################################################################################
### At the root page of the server
@app.route('/')
def serveLogin():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

#########################################################################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # Handle user login.
    # If the request method is POST, check the username and password.
    # If valid, store the username in the session and redirect to the aircraft page.
    # Otherwise, reload the login page with an error message.
    
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Simple check: In a real application, this should query the database
        if username in users and check_password_hash(users[username], password):
            # Store the username in the session
            session['username'] = username
            flash('You were successfully logged in', 'success')
            # Redirect to the aircraft page
            return redirect(url_for('homePage'))
        else:
            # Flash an error message if credentials are invalid
            flash('Invalid username or password', 'danger')
            # Redirect back to the login page
            return redirect(url_for('login'))
    
     # Render the login template on a GET request
    return render_template('login.html')

#########################################################################################
@app.route('/logout')
def logout():
    
    # Handle user logout.
    # Remove the username from the session and redirect to the login page.
    
    # Remove the username from the session
    session.pop('username', None)
    flash('You were successfully logged out', 'success')
    # Redirect to the login page
    return redirect(url_for('login'))

#########################################################################################
@app.route('/home')
def homePage():

    # Display the aircraft management page.
    # If the user is not logged in, redirect to the login page.

    if 'username' not in session:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))
    # Render the aircraft management page
    return render_template('home.html')

#########################################################################################
@app.route('/homeData', methods=['GET'])
def get_aircraft_data():

    #  Provide JSON data of all aircraft.
    # This endpoint is used by the aircraft management page to load data.

    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Fetch all aircraft data from the database
    taskList = pd.DataFrame(taskDAO.getLDND())
    #print("taskList:{}".format(taskList["TASK\nNUMBER"])
    # converting a it to a list of dictionaries from a list
    mpdData = []
    for index, task in taskList.iterrows():
        #print("task:{}. index:{}".format(task["TASK\nNUMBER"], index))
        taskDict = {
            "TASKNUMBER": task["TASK\nNUMBER"],
            "SOURCETASK": task["SOURCE TASK\nREFERENCE"],
            "ACCESS": task["ACCESS"],
            "PREPARATION": task["PREPARATION"],
            "ZONE": task["ZONE"],
            "DESCRIPTION": task["DESCRIPTION"],
            "TASKCODE": task["TASK CODE"],
            "SAMPLETHRES": task["SAMPLE\nTHRESHOLD"],
            "SAMPLEINT": task["SAMPLE\nINTERVAL"],
            "100%THRES": task["100%\nTHRESHOLD"],
            "100%INT": task["100%\nINTERVAL"],
            "SOURCE": task["SOURCE"],
            "REFERENCE": task["REFERENCE"],
            "APPLICABILITY": task["APPLICABILITY"]
        }
        # Convert NaN to None (so JSON treats it as 'null')
        for key, value in taskDict.items():
            if pd.isna(value):  # Check for NaN values
                taskDict[key] = ''  # Convert to Non
        
        for key, value in taskDict.items():
            if isinstance(value, str):  # Check for NaN values
                taskDict[key] = value.replace("\n", "<br>")
        
        mpdData.append(taskDict)

    # Return the data in JSON format
    #print(mpdData)
    #print("Jsonify:{}".format(jsonify(mpdData)))


    return jsonify(mpdData)

msn = None

#########################################################################################
@app.route('/msnData', methods=['POST'])
def get_msn_data():
    """Handles the request for MSN data and returns applicable values."""
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    msn = data.get("msn", "").strip()
    if not msn:
        return jsonify({"error": "Invalid MSN"}), 400

    # Fetch conditions from database
    applicabilities = list(taskDAO.addMSN(msn))

    # Return only the new column as JSON list
    return jsonify(applicabilities)

#########################################################################################
@app.route('/download')
def download_mpd():
    if 'username' not in session:
        return redirect(url_for('login'))

    output = taskDAO.getCopy()  # Get the in-memory file
    return send_file(output, as_attachment=True, download_name="MPD_File.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


#########################################################################################
#########################################################################################
#########################################################################################
# Main entry point for the Flask application
if __name__ == "__main__":
     # Run the Flask development server
    app.run(debug=True)