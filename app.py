# Import the dependencies.
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import flask
from flask import Flask , jsonify
#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite',
                       connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"***Welcome to the home page***<br/>"
        f"All Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f" /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():

    latest_prcp = session.query((Measurement.date), Measurement.prcp)\
    .filter(Measurement.date > '2016-08-22')\
    .filter(Measurement.date <= '2017-08-23')\
    .order_by(Measurement.date).all()

    # convert results to a dictionary with date as key and prcp as value
    prcp_dictionary = dict(latest_prcp)

    # return json list of dictionary
    return jsonify(prcp_dictionary)



@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.name, Station.station).all()

    # convert results to a dict
    stations_dict = dict(stations)

    # return json list of dict (I decided to do a dict instead of a list here to show both the station name and the station number)
    return jsonify(stations_dict)


@app.route("/api/v1.0/tobs")
def tobs():

    tobs= session.query((Measurement.date), Measurement.tobs)\
    .filter(Measurement.date > '2016-08-23')\
    .filter(Measurement.date <= '2017-08-23')\
    .filter(Measurement.station == "USC00519281")\
    .order_by(Measurement.date).all()

    # convert results to dict(I decided to to a dict here instead of a list in order to show the dates along with the temperature for each date)
    tobs_dictionary = dict(tobs)

    # return json list of dict
    return jsonify(tobs_dictionary)


@app.route('/api/v1.0/<start>')
def get_t_start(start):
    session = Session(engine)
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    tobsall = []
    for min,avg,max in query:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

@app.route('/api/v1.0/<start>/<stop>')
def get_t_start_stop(start,stop):
    session = Session(engine)
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    tobs_list = []
    for min,avg,max in query:
        tobs_dictionary = {}
        tobs_dictionary["Min"] = min
        tobs_dictionary["Average"] = avg
        tobs_dictionary["Max"] = max
        tobs_list.append(tobs_dictionary)

    return jsonify(tobs_list)
    



if __name__ == '__main__':
    app.run(debug=True)