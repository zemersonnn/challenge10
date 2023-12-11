# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Homepage
@app.route("/")
def homepage():
    """List all available routes."""

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation 
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    # Query
    results = session.query(measurement.prcp).all()

    session.close()

    prcp_data = list(np.ravel(results))

    # Return the JSON representation of your dictionary.
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station_list():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query
    results = session.query(measurement.station).distinct().all()

    session.close()

    station_list = list(np.ravel(results))

    # Return the JSON representation of your dictionary.
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set.
    yr_ago_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Preform a query to retrieve the dates and temperature observations of the most active station for the previous year of data.
    active_station = session.query(measurement.date, measurement.tobs).filter(measurement.station== 'USC00519281').\
                            filter(measurement.date >= yr_ago_date).all()
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary from the row data and append to list most_active
    most_active = []
    for date, temp in active_station:
        active_dict = {}
        active_dict[date] = temp
        most_active.append(active_dict)
        
    return jsonify(most_active)

# Start 
@app.route("/api/v1.0/<start>")
def start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.date >= start).all()
    
    # Close Session                                                  
    session.close()
    
    start_date = []
    for min, max, avg in query_results:
        start_dict = {}
        start_dict["Minimum Temperature"] = min
        start_dict["Maxium Temperature"] = max
        start_dict["Average Temperature"] = avg
        start_date.append(start_dict)
        
    return jsonify(start_date)

# Range
@app.route("/api/v1.0/<start>/<end>")
def range_date(start,end):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    query_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    # Close Session                                                  
    session.close()
    
    range_date = []
    for min, max, avg in query_results:
        range_dict = {}
        range_dict["Minimum Temperature"] = min
        range_dict["Maxium Temperature"] = max
        range_dict["Average Temperature"] = avg
        range_date.append(range_dict)
        
    return jsonify(range_date)

if __name__ == '__main__':
    app.run(debug=True)






 

    
