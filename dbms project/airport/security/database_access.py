import mysql.connector

# Function to insert data into the AircraftDetails table
def insert_aircraft_details(cursor, aircraft_data):
    sql = "INSERT INTO AircraftDetails (FlightNumber, AircraftType, Manufacturer, Model, Capacity, CurrentLocation, LastMaintenanceDate, NextMaintenanceDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, aircraft_data)

# Function to insert data into the Gates table
def insert_gates(cursor, gate_data):
    sql = "INSERT INTO Gates (GateID, GateNumber, Terminal, Status) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, gate_data)

# Function to insert data into the Arrivals table
def insert_arrivals(data_list,data_list2,data_list3):
    # Establish connection to the AirportDB
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    
    cursor = conn.cursor()
    
    # SQL insert statement
    sql = """
    INSERT INTO Arrivals (ArrivalID, FlightNumber, ArrivalDateTime, Origin, GateID, Status) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    # Convert the string into a tuple of appropriate data types
    arrival_data = tuple(data_list)
    cursor.execute(sql, arrival_data)

    conn.commit()
    
    sql = """
    INSERT INTO Departures (DepartureID, FlightNumber, DepartureDateTime, Destination, GateID, Status) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    departure_data = tuple(data_list2)
    cursor.execute(sql, departure_data)

    conn.commit()

    sql = """
    INSERT INTO Flightschedule (ScheduleID, FlightNumber, DepartureDateTime, ArrivalDateTime, Status) 
    VALUES (%s, %s, %s, %s, %s)
    """
    flightsc_data = tuple(data_list3)
    cursor.execute(sql, flightsc_data)


    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()


def get_flight_schedule(cursor):
    # Define the SQL query to fetch all rows from the FlightSchedule table
    sql = "SELECT * FROM FlightSchedule"
    cursor.execute(sql)
    
    # Fetch all rows from the executed query
    rows = cursor.fetchall()
    
    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    
    # Convert rows into a list of dictionaries
    flight_schedule_list = [dict(zip(column_names, row)) for row in rows]
    
    return flight_schedule_list


def insert_passenger(data_list,data_list2):
    # Establish connection to the AirportDB
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    
    cursor = conn.cursor()

    sql = """
    INSERT INTO Passengers (PassengerID, name, age, gender, contactinformation,FlightNumber,seatnumber) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    passenger_data = tuple(data_list)
    cursor.execute(sql, passenger_data)

    conn.commit()

    sql = """
    INSERT INTO baggage (baggageID, PassengerID, Weight, Status) 
    VALUES (%s, %s, %s, %s)
    """
    baggage_data = tuple(data_list2)
    cursor.execute(sql, baggage_data)


    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

def get_flight_numbers_not_at_airport(cursor):
    # Define the SQL query to fetch flight numbers at the airport
    sql = "SELECT FlightNumber FROM AircraftDetails WHERE UPPER(CurrentLocation) = 'NOT AT AIRPORT'"
    cursor.execute(sql)
    
    # Fetch all rows from the executed query
    rows = cursor.fetchall()
    
    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    
    # Convert rows into a list of dictionaries
    flight_numbers_list = [dict(zip(column_names, row)) for row in rows]
    print(flight_numbers_list)
    
    return flight_numbers_list

def get_flight_numbers_at_airport(cursor):
    # Define the SQL query to fetch flight numbers at the airport
    sql = "SELECT FlightNumber FROM AircraftDetails WHERE UPPER(CurrentLocation) = 'AT AIRPORT'"
    cursor.execute(sql)
    
    # Fetch all rows from the executed query
    rows = cursor.fetchall()
    
    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    
    # Convert rows into a list of dictionaries
    flight_numbers_list = [dict(zip(column_names, row)) for row in rows]
    print(flight_numbers_list)
    return flight_numbers_list

def up_passenger(uppassenger_data,upbaggage_data):
    # Establish connection to the AirportDB
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    
    cursor = conn.cursor()

    sql = """
    UPDATE Passengers 
    SET name = %s, 
        age = %s, 
        gender = %s, 
        contactinformation = %s, 
        FlightNumber = %s, 
        seatnumber = %s
    WHERE PassengerID = %s 
    """

    
    cursor.execute(sql, uppassenger_data)

    conn.commit()

    sql = """
    UPDATE Baggage 
    SET Weight = %s, 
        Status = %s
    WHERE BaggageID = %s and PassengerID = %s
    """
  
    cursor.execute(sql, upbaggage_data)


    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()



def delete_passenger(d_data):

    # Establish connection to the AirportDB
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    cursor = conn.cursor()
    # Delete the passenger
    del_data=tuple(d_data)
    cursor.execute("DELETE FROM Baggage WHERE PassengerID = %s", del_data)

    conn.commit()
    cursor.execute("DELETE FROM Passengers WHERE PassengerID = %s", del_data)
    

    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()


# Function to update the Arrivals table
def update_arrival(data):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    cursor = conn.cursor()

    sql = """
    UPDATE Arrivals
    SET ArrivalDateTime = %s, Status = %s
    WHERE ArrivalID = %s
    """
    data2=data[1:]
    sql2="""
    update FlightSchedule
    set Status = %s where ScheduleId = %s"""
    cursor.execute(sql, data)
    cursor.execute(sql2, data2)
    conn.commit()
    cursor.close()
    conn.close()

# Function to update the Arrivals table
def update_departure(data):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    cursor = conn.cursor()

    sql = """
    UPDATE Departures
    SET DepartureDateTime = %s, Status = %s
    WHERE DepartureID = %s
    """
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

# Function to delete a record from the specified table
def delete_record(table, record_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    cursor = conn.cursor()
    
    if table == "Arrivals":
        sql = "DELETE FROM Arrivals WHERE FlightNumber = %s"
    elif table == "Departures":
        sql = "DELETE FROM Departures WHERE FlightNumber = %s"
    sql3="DELETE FROM Baggage WHERE Baggage.PassengerID IN (select PassengerID from Passengers where FlightNumber = %s)"
    cursor.execute(sql3, (record_id,))
    conn.commit()
    sql2 = "DELETE FROM Passengers WHERE FlightNumber = %s"

    cursor.execute(sql, (record_id,))
    cursor.execute(sql2, (record_id,))
    conn.commit()
    cursor.close()
    conn.close()


if __name__=="__main__":
    conn = mysql.connector.connect(host="localhost", user="root", password="password",database="AirportDB")

    if conn.is_connected():
        print("Connected to MySQL database")
    else:
        print("Failed to connect to MySQL database")
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    flight_schedule = get_flight_schedule(cursor)
    print(flight_schedule)
    # Close the cursor and connection
    cursor.close()
    conn.close()

