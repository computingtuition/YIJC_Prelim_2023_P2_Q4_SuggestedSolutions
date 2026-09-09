#### THIS IS Task4_2.py ####

import Task4_1 # to run Task 4.1 code

import flask
import sqlite3

app = flask.Flask(__name__)

@app.route('/')
def home():
    # renders login page
    return flask.render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    # obtain form data
    # should be a dictionary of one key-value, driverID
    data = flask.request.form

    # check the db file if the driverID exists
    db = sqlite3.connect('Taxi.db')

    cursor = db.execute('''
      SELECT ID, name
      FROM Driver
      WHERE ID = ?
    ''', (data.get('driverID'),))

    # there should only be one driver matching the ID, if found
    # we use fetchone() to obtain the driver's tuple directly
    # or it will return None if not found
    driver = cursor.fetchone()

    # to render the next page, we also need vehicle details
    cursor = db.execute('''
      SELECT License, Model, MaxPassenger
      FROM Vehicle
    ''')

    # there should only be one driver matching the ID, if found
    # we use fetchone() to obtain the driver's tuple directly
    # or it will return None if not found
    vehicles = cursor.fetchall()
    
    db.close()

    # if no entries found, means driverID was wrong, do a error message
    if driver == None:
        return 'Error, Driver ID does not exist'
        
    # render the rental page
    return flask.render_template('rental.html', driver=driver, vehicles=vehicles)


@app.route('/rental', methods=['POST'])
def menu():
    # should contain 3 key-value pairs - driverID, rentalDate, vehicle
    data = flask.request.form

    # perform a query check on the database for the vehicle’s availability on the selected date
    db = sqlite3.connect('Taxi.db')

    # check is someone has rented the vehicle on this date
    cursor = db.execute('''
        SELECT DriverID
        FROM Rent
        WHERE License = ?
        AND Date = ?
    ''', (data.get('vehicle'), data.get('rentalDate')))

    # there should only be 1 rental for each vehicle per day
    # so, we use fetchone() to obtain the tuple containing driverID of the rental
    # or returns None if nobody rented it that day
    rented = cursor.fetchone()

    if rented != None:        
        db.close()   
        # render a simple message (no template needed)
        return 'Vehicle unavailable for the selected date.'

    else:
        # record the details in the database's table Rent with the field Paid indicated as “No”
        db.execute('''
            INSERT INTO Rent(DriverID, License, Date, Paid)
            VALUES(?, ?, ?, ?)
        ''', (data.get('driverID'), data.get('vehicle'), data.get('rentalDate'), 'No'))

        db.commit()

        ### FOR TASK 4.4 - simple message
        # return 'Rental Successful.'

        ### FOR TASK 4.5 - query on the database for the driver's rentals (all rentals included paid, referring to screenshot on question)
        cursor = db.execute('''
            SELECT Rent.Date, Vehicle.Model, Vehicle.Cost, Rent.Paid
            FROM Rent, Vehicle
            WHERE Rent.License = Vehicle.License
            AND Rent.DriverID = ?
        ''', (data.get('driverID'),)) # remember , for single item tuple   
        driver_rental = cursor.fetchall()

        # compute the outstanding total rental owed (not paid)
        owed = 0
        for rent_detail in driver_rental:
            if rent_detail[3] == 'No':
                owed += float(rent_detail[2])
        
        # render the success.html to display a table as shown in question
        db.close() 
        return flask.render_template('success.html', owed='{:.2f}'.format(owed), rentals=driver_rental)
        
  

# this is only for deployment on Google Cloud (so that you can preview online)
app.run('0.0.0.0', port=8080)

# for running on own computer, use this
# app.run()
