# Step 2 - Climate App
#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Dependencies and Setup
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

session = Session(engine)

# Home page
@app.route("/")
def homepage():
    return(
        f"Available routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_data_point = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    
    precipitation = []
    for date, prcp in precipitation_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    #station_results = session.query(Station.station, Station.name).group_by(Station.station).all()
    station_results = session.query(Station.name).all()
    station_names = list(np.ravel(station_results))
    return jsonify(station_names)

# Tobs
@app.route("/api/v1.0/tobs")
def tobs():
    last_data_point = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    return jsonify(tobs_results)

# Start
@app.route("/api/v1.0/<start>")
def trip(start):
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    tobs_start = list(np.ravel(start_results))
    return jsonify(tobs_start)
   
# Start/End
@app.route("/api/v1.0/<start>/<end>")
def trips(start, end):
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    tobs_start_end = list(np.ravel(start_end_results))
    return jsonify(tobs_start_end)
    
if __name__ == '__main__':
    app.run(debug=True)                   
                          