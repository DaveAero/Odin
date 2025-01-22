# Thor.py
# DAO for updating the database
# By David Burke


#########################################################################################
# Import required functions

#########################################################################################
# The Main AircraftDAO class
class AircraftDAO:
    connection= ""
    cursor =    ''
    
    def getCursor(self): 

        # Establish a connection to the MySQL database using provided configuration.

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):

        # Close the database cursor and connection.

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def create(self, values):

        # Insert a new aircraft record into the database.

        cursor = self.getCursor()
        sql = """
        INSERT INTO aircraft (
            model_name, manufacturer, aircraft_serial_number, configuration, 
            last_flight, certificate_of_airworthiness, country_of_origin, 
            country_of_registration, engine_type
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # put the values into database using the sql insctructions
        cursor.execute(sql, values)
        self.connection.commit()
        # Getting back out the latest ID used to be sent to the HTML to update table in browser memory
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def getAll(self):

        # Retrieve all aircraft records from the database.

        cursor = self.getCursor()
        sql = """
        SELECT 
            aircraft_id,
            model_name,
            manufacturer,
            aircraft_serial_number,
            configuration,
            DATE_FORMAT(last_flight, '%Y-%m-%d') AS last_flight,  
            certificate_of_airworthiness,
            country_of_origin,
            country_of_registration,
            engine_type
        FROM aircraft;
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeAll()
        return result

    def findByID(self, id):

        # Finding just one aircraft

        cursor = self.getCursor()
        sql = "SELECT * FROM aircraft WHERE aircraft_id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        self.closeAll()
        return result

    def update(self, values):

        # Update an aircraft in the mysql database

        cursor = self.getCursor()
        sql = """
        UPDATE aircraft
        SET model_name = %s, 
            manufacturer = %s, 
            aircraft_serial_number = %s, 
            configuration = %s, 
            last_flight = %s, 
            certificate_of_airworthiness = %s, 
            country_of_origin = %s, 
            country_of_registration = %s, 
            engine_type = %s
        WHERE aircraft_id = %s
        """
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def delete(self, id):

        # Delete an aircraft from the mysql database

        cursor = self.getCursor()
        sql = "DELETE FROM aircraft WHERE aircraft_id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

# Example usage
aircraftDAO = AircraftDAO()