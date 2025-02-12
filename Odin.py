# Odin.py
# The main Rust server
# By David Burke


#########################################################################################
# Import required functions
from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
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

@app.route('/home')
def homePage():

    # Display the aircraft management page.
    # If the user is not logged in, redirect to the login page.

    if 'username' not in session:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for('login'))
    # Render the aircraft management page
    return render_template('home.html')

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
    mpdConditions = pd.DataFrame(taskDAO.conditions())

    if "condition" not in mpdConditions.columns:
        return jsonify({"error": "Invalid data format"}), 500

    # Create a new column dynamically using the MSN value
    column_name = f"MSN {msn}"
    mpdConditions[column_name] = ""

    # Apply the condition (from line 168-170)
    for index, row in mpdConditions.iterrows():
        conditionlist = row["condition"]
        condition = conditionlist[0]
        if condition[0] == "ALL":
            mpdConditions.at[index, column_name] = "Applicable"

    # Return only the new column as JSON list
    return jsonify(mpdConditions[column_name].tolist())

#########################################################################################
#########################################################################################
#########################################################################################

# Retrieve all aircraft
@app.route('/aircraft', methods=['POST'])
def createAircraft():

    # Handle the creation of a new aircraft.
    # Receive aircraft data from the request and insert it into the database.

    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Putting the aircraft data into a dictionary
    aircraft = {
        "model_name": request.json.get("model_name"),
        "manufacturer": request.json.get("manufacturer"),
        "aircraft_serial_number": request.json.get("aircraft_serial_number"),
        "configuration": request.json.get("configuration"),
        "last_flight": request.json.get("last_flight"),
        "certificate_of_airworthiness": request.json.get("certificate_of_airworthiness"),
        "country_of_origin": request.json.get("country_of_origin"),
        "country_of_registration": request.json.get("country_of_registration"),
        "engine_type": request.json.get("engine_type"),
    }
    # Insert the new aircraft into the database using DAO. The my DAO server will return the aircraft id
    aircraftID = taskDAO.create(tuple(aircraft.values()))
    # Getting the aircraft id from the update mysql 
    aircraft["aircraft_id"] = aircraftID
    # Return the new aircraft in JSON format
    return jsonify(aircraft), 201


#########################################################################################
# Retrieve aircraft by id
@app.route('/aircraft/<int:id>')
def findAircraftById(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    aircraft = taskDAO.findByID(id)
    if aircraft is None:
        return jsonify({}), 204
    return jsonify(aircraft)  

#########################################################################################
# Update existing aircraft
# curl -X "PUT" -d "{\"Title\":\"New Title\", \"Price\":999}" -H "content-type:application/json" http://127.0.0.1:5000/books/1
@app.route('/aircraft/<int:id>', methods=['PUT'])
def updateAircraft(id):

    # Handle the update of an existing aircraft.
    # Receive updated aircraft data and update it in the database.

    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Getting current aircraft data from the mysql server
    aircraft = taskDAO.findByID(id)
    if aircraft is None:
        return jsonify({}), 404
    
    if not request.json:
        abort(400)
    
    # Converting the tuple returned by findByID to a dictionary
    foundAircraft = {
        "model_name": aircraft[1],
        "manufacturer": aircraft[2],
        "aircraft_serial_number": aircraft[3],
        "configuration": aircraft[4],
        "last_flight": aircraft[5],
        "certificate_of_airworthiness": aircraft[6],
        "country_of_origin": aircraft[7],
        "country_of_registration": aircraft[8],
        "engine_type": aircraft[9],
        "aircraft_id": aircraft[0]
    }

    # Getting the updated info from the html request
    reqJson = request.json

    # Update the dictionary with the new values from the request
    foundAircraft['model_name'] = reqJson.get('model_name', foundAircraft['model_name'])
    foundAircraft['manufacturer'] = reqJson.get('manufacturer', foundAircraft['manufacturer'])
    foundAircraft['aircraft_serial_number'] = reqJson.get('aircraft_serial_number', foundAircraft['aircraft_serial_number'])
    foundAircraft['configuration'] = reqJson.get('configuration', foundAircraft['configuration'])
    foundAircraft['last_flight'] = reqJson.get('last_flight', foundAircraft['last_flight'])
    foundAircraft['certificate_of_airworthiness'] = reqJson.get('certificate_of_airworthiness', foundAircraft['certificate_of_airworthiness'])
    foundAircraft['country_of_origin'] = reqJson.get('country_of_origin', foundAircraft['country_of_origin'])
    foundAircraft['country_of_registration'] = reqJson.get('country_of_registration', foundAircraft['country_of_registration'])
    foundAircraft['engine_type'] = reqJson.get('engine_type', foundAircraft['engine_type'])

    # Converting to a tuple for the mysql server
    updated_aircraft = tuple(foundAircraft.values())

    # Pass the tuple to the update method
    #print(updated_aircraft)
    taskDAO.update(updated_aircraft)
    
    return jsonify(foundAircraft)

#########################################################################################
# Delete aircraft
@app.route('/aircraft/<int:id>', methods=['DELETE'])
def deleteAircraft(id):

    # Handle the deletion of an aircraft.
    # Remove the specified aircraft from the database.

    if 'username' not in session:
        return redirect(url_for('login'))
    
    aircraft = taskDAO.findByID(id)
    if aircraft is None:
        return jsonify({}), 404
    
    # Delete the aircraft from the database using DAO
    taskDAO.delete(id)
    # Return a success message
    return jsonify({"status": "success"}), 200

#########################################################################################
#########################################################################################
#########################################################################################
# Main entry point for the Flask application
if __name__ == "__main__":
     # Run the Flask development server
    app.run(debug=True)