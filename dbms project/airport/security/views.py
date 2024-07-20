from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from security.database_access import get_flight_schedule,insert_arrivals,get_flight_numbers_not_at_airport,insert_passenger,get_flight_numbers_at_airport,up_passenger,delete_passenger,update_arrival,update_departure,delete_record
import mysql.connector

def fl_no(negate=1):
    # Establish connection to the AirportDB
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="AirportDB"
    )
    cursor = conn.cursor()
    
    # Fetch flight numbers at the airport
    if negate==1:
        context = {
            'posts': get_flight_numbers_not_at_airport(cursor)
        }
    else:
        context = {
            'posts': get_flight_numbers_at_airport(cursor)
        }
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    return context

def cust(request):
    context=fl_no()
    return render(request,'security/fl_no.html',context)


def base(request):
    return render(request,'security/base.html')

def schedule(request):
  conn = mysql.connector.connect(host="localhost", user="root", password="password",database="AirportDB")
  cursor = conn.cursor()
  context ={
    'posts' : get_flight_schedule(cursor)
  }
  # Close the cursor and connection
  cursor.close()
  conn.close()

  return render(request,'security/schedule.html',context)

def arrival_success(request):
    return render(request, 'security/arrival_success.html')

def add_arrival(request):
    if request.method == 'POST':
        # Extract data from request.POST
        arrival_id = int(request.POST.get('ArrivalID'))
        flight_number = request.POST.get('FlightNumber')
        arrival_datetime = request.POST.get('ArrivalDateTime')
        departure_datetime = request.POST.get('DepartureDateTime')
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        gate_id = int(request.POST.get('GateID'))
        status = request.POST.get('Status')

        # Convert data to a list of strings
        arrival_data = [
            arrival_id,
            flight_number,
            arrival_datetime,
            origin,
            gate_id,
            status
        ]

        departure_data = [
            arrival_id,
            flight_number,
            departure_datetime,
            destination,
            gate_id,
            status
        ]
        
        flightsc_data = [
            arrival_id,
            flight_number,
            departure_datetime,
            arrival_datetime,
            status
        ]

        # Print the list to the console or use it as needed
        print(arrival_data)
        insert_arrivals(arrival_data,departure_data,flightsc_data)

        return redirect('arrival_success')  # Redirect to a success page or another view
    else:
        context=fl_no()
        return render(request, 'security/add_arrival.html',context)
    

def passenger_success(request):
    return render(request, 'security/passenger_success.html')

def add_passenger(request):
    if request.method == 'POST':
        # Extract data from request.POST
        passenger_id = int(request.POST.get('PassengerID'))
        flight_number = request.POST.get('FlightNumber')
        name = request.POST.get('Name')
        age = request.POST.get('Age')
        gender = request.POST.get('Gender')
        contact_information = request.POST.get('ContactInformation')
        seat_number = int(request.POST.get('SeatNumber'))
        baggage_weight = request.POST.get('BaggageWeight')
        status = 'Boarded'

        # Convert data to a list of strings
        passenger_data = [
            passenger_id,
            name,
            age,
            gender,
            contact_information,
            flight_number,
            seat_number
        ]

        baggage_data = [
            passenger_id,
            passenger_id,
            baggage_weight,
            status
        ]

        insert_passenger(passenger_data,baggage_data)
        return redirect('passenger_success')
    else:
        context=fl_no(0)
        return render(request, 'security/add_passenger.html',context)
    
def update_passenger(request):
    if request.method == 'POST':
        # Extract data from request.POST
        passenger_id = int(request.POST.get('PassengerID'))
        flight_number = request.POST.get('FlightNumber')
        name = request.POST.get('Name')
        age = request.POST.get('Age')
        gender = request.POST.get('Gender')
        contact_information = request.POST.get('ContactInformation')
        seat_number = int(request.POST.get('SeatNumber'))
        baggage_weight = request.POST.get('BaggageWeight')
        status = 'Boarded'

        # Convert data to a list of strings
        uppassenger_data = [
            name,
            age,
            gender,
            contact_information,
            flight_number,
            seat_number,
            passenger_id,
        ]

        upbaggage_data = [
            baggage_weight,
            status,
            passenger_id,
            passenger_id,
        ]

        up_passenger(uppassenger_data,upbaggage_data)
        return redirect('passenger_success')
    else:
        return render(request, 'security/update_passenger.html')

def delete_passenger_success(request):
    return render(request, 'security/delete_passenger_success.html')

def get_passenger_ids(cursor):
    sql = "SELECT PassengerID as id FROM Passengers"
    cursor.execute(sql)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    passenger_ids = [dict(zip(column_names, row)) for row in rows]
    return passenger_ids


def del_passenger(request):
    if request.method == 'POST':
        passenger_id = request.POST.get('PassengerID')
        
        delete_passenger(passenger_id)
        return redirect('delete_passenger_success')
    else:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="AirportDB"
        )
        cursor = conn.cursor()
        passenger_ids = get_passenger_ids(cursor)  # Default to fetching Arrival IDs
        cursor.close()
        conn.close()

        context = {
            'passenger_ids': passenger_ids
        }
        return render(request, 'security/delete_passenger.html', context)

def update_success(request):
    return render(request, 'security/update_success.html')

# Function to fetch Arrival IDs
def get_arrival_ids(cursor):
    sql = "SELECT ArrivalID FROM Arrivals"
    cursor.execute(sql)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    arrival_ids = [dict(zip(column_names, row)) for row in rows]
    print(arrival_ids)
    return arrival_ids

def update_arrival_view(request):
    if request.method == 'POST':
        arrival_id = int(request.POST.get('ArrivalID'))
        arrival_datetime = request.POST.get('ArrivalDateTime')
        departure_datetime = request.POST.get('DepartureDateTime')
        status = request.POST.get('Status')

        update_data = (arrival_datetime, status, arrival_id)
        update_arrival(update_data)
        departure_update_data=(departure_datetime,status,arrival_id)
        update_departure(departure_update_data)
        return redirect('update_success')  # Redirect to a success page or another view

    else:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="AirportDB"
        )
        cursor = conn.cursor()
        arrival_ids = get_arrival_ids(cursor)
        cursor.close()
        conn.close()

        context = {
            'arrival_ids': arrival_ids
        }
        return render(request, 'security/update_arrival.html', context)

def get_record_ids(cursor, table):
    if table == "Arrivals":
        sql = "SELECT FlightNumber as id FROM Arrivals"
    elif table == "Departures":
        sql = "SELECT FlightNumber as id FROM Departures"
    cursor.execute(sql)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    record_ids = [dict(zip(column_names, row)) for row in rows]
    return record_ids

def delete_success(request):
    return render(request, 'security/deletion_success.html')

def delete_record_view(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        
        delete_record("Arrivals", record_id)
        delete_record("Departures",record_id)
        return redirect('delete_success')  # Redirect to a success page or another view

    else:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="AirportDB"
        )
        cursor = conn.cursor()
        record_ids = get_record_ids(cursor, "Arrivals")  # Default to fetching Arrival IDs
        cursor.close()
        conn.close()

        context = {
            'record_ids': record_ids
        }
        return render(request, 'security/del_ar_del.html', context)