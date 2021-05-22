import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save reference to the table

measurement = base.classes.measurement
station= base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Import Flask
from flask import Flask, jsonify

# Create an app
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")



#Define what to do when a user hits the /api/v1.0/precipation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for the 'precipitation' page...")
    # Create a session to the database 
    session = Session(bind=engine)

    # Find the most recent date in the data set (2 ways to do it)
    recent_date = engine.execute('select date from measurement order by date desc limit 1').fetchall()
    recent_date
    # Starting from the most recent data point in the database.
    year = engine.execute("select date from measurement where date > '2016-08-23'").fetchall()
   

    # Perform a query to retrieve the data and precipitation scores
   prcpdate = engine.execute("select date,prcp from measurement where date > '2016-08-23'").fetchall()

    session.close()

    prcp_tuple = list(np.ravel(prcpdate))

    return jsonify(prcp_tuple)   


#Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for the 'stations' page...")
    # Create a session to the database 
    session = Session(engine)

    stations_list = engine.execute("select station from station").fetchall()
    
    session.close()

    stations_tuple = list(np.ravel(stations_list))

    return jsonify(stations_tuple) 




  

if __name__ == "__main__":
    app.run(debug=True)