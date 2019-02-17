from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlite3

def create_db_connect():
    database = "Resources\hawaii.sqlite"
    connection = sqlite3.connect(database)
    return (connection)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome - Below are the available routes<br/>"
        f"/api/v1.0/Precipitation<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/TOBS<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/Precipitation")
def Precipitation():
    conn = create_db_connect()
    with conn:
        Precipitation_Info = conn.execute("select date, prcp from Measurement").fetchall()
    return jsonify(dict(Precipitation_Info))

@app.route("/api/v1.0/Stations")
def station():
    conn = create_db_connect()
    with conn:
        Station_Data = conn.execute("select station, name from station order by name").\
                        fetchall()
    return jsonify(Station_Data)

@app.route("/api/v1.0/TOBS")
def TOBS():
    conn = create_db_connect()
    with conn:
        Max_Date = conn.execute("select max(date) from Measurement").fetchall()
        Date = []
        Date = list(np.ravel(Max_Date))
        for word in Date:
            trip_end_date = '2017-12-31'
            year = trip_end_date[0:4]
            month = trip_end_date[5:7]
            day = trip_end_date[8:10]
        Max_Date = dt.date(int(year), int(month), int(day))
        Previous_Year = Max_Date - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
        tobs_data = conn.execute("select date, prcp from Measurement").fetchall()
        tobs_dict = dict(tobs_data)
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    conn = create_db_connect()
    with conn:
        result_dict = conn.execute("select station, min(tobs), max(tobs), avg(tobs) from Measurement where date >= ? group by(station)", (start_date,)).fetchall()
    return jsonify(result_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):
    conn = create_db_connect()
    with conn:
        result_dict = conn.execute("select station, min(tobs), max(tobs), avg(tobs) from Measurement where date >= ? and date <= ? group by(station)", (start_date,end_date,)).fetchall()
    return jsonify(result_dict)

if __name__ == "__main__":
    app.run(debug=True)