import os
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/ChicagoRestaurants.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Restaurants = Base.classes.RestaurantData


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

######################################################################
#############         SHOW ME ALL OF THE COLUMNS I CAN GET  ##########
######################################################################
@app.route("/AvailableColumns")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Restaurants).statement
        #stmt = db.session.query(Restaurants).statement

    df = pd.read_sql_query(stmt, db.session.bind)
    return jsonify(list(df))

######################################################################
####################            SHOW ME ALL OF THE DATA   ############
######################################################################

@app.route("/data")
def RestaurantList():

    #available columns:  ["id","Name","DBA","identifier","Type","Risk","Street","City",\
    # "State","Zip","Date","Inspection","Success","Description","Lat","Lng"]
    results = db.session.query(Restaurants.Name, Restaurants.DBA, Restaurants.Type, Restaurants.Street, Restaurants.City, \
        Restaurants.State, Restaurants.Date, Restaurants.Inspection, Restaurants.Success, Restaurants.Description, \
            Restaurants.Lat, Restaurants.Lng).limit(3000) #change this to  ".all()" to retrive all the data
            #Note-- the year function returns Null when adding strftime. Need to FIX: func.strftime("%YYYY", Restaurants.Date)
        
    list = []
    for result in results:
        list.append({
            #"Name": result[0],
            "DBA": result[1],
            "Lat": result[11],
            "Lng":result[10],
            "Inspection":result[7],
            "success":result[8],
            "Year": result[6]
           
        })
    return jsonify(list)
######################################################################
####################FILTER BY INSPECTION DATE#########################
######################################################################

####NOTE: NEED TO FIC THIS TO TAKE IN A DATE VARIABLE

@app.route("/InspectionDate")
def inspectiondate():

    #available columns:  ["id","Name","DBA","identifier","Type","Risk","Street","City",\
    # "State","Zip","Date","Inspection","Success","Description","Lat","Lng"]
    years = db.session.query(Restaurants.Name, Restaurants.DBA, Restaurants.Type, Restaurants.Street, Restaurants.City, \
        Restaurants.State, Restaurants.Date, Restaurants.Inspection, Restaurants.Success, Restaurants.Description, \
            Restaurants.Lat, Restaurants.Lng).filter_by(Date="06/06/2019").all()
    list = []
    for result in years:
        list.append({
            "Name": result[0]
        })
    return jsonify(list)



if __name__ == "__main__":
    app.run()