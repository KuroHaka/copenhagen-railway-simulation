# importing Flask and other modules
from flask import Flask, request, render_template
from datetime import datetime, timedelta

import json, os, sys
#from train_simulation.Person import Person
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)
new_model_file = open(os.path.join(dirname, '../assets/model.json'), mode="w", encoding="utf-8")
from train_simulation.Person import Person

trains = []
carriers=[]


app = Flask(__name__)  #flask constructor

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])

def Run_Simulation():  # process functions
    if request.method == "POST":
       print(os.pardir)
       # getting input with name = fname in HTML form
       Number_of_Persons=request.form.get("number_of_persons")
       Number_of_Trains=request.form.get("number_of_trains/carriers")
       Transport_Types=request.form.get("switchers")
       Slected_Stations=request.form.getlist('mymultiselect')
       Start_Time=request.form.get("start_time")
       End_Time=request.form.get("end_time")

       print(request.form.getlist('mymultiselect'))

       if Transport_Types=='Trains':
            pass
       elif Transport_Types=='Carriers':
            pass

       Person.create_passengers( Slected_Stations,{'start':datetime.strptime(str(Start_Time),'%H:%M'),'end': datetime.strptime(str(End_Time),'%H:%M')}, Number_of_Persons)
       return "The input information is, " + "Number_of_Trains: " + Number_of_Trains +"; Number_of_Persons: "+Number_of_Persons+";  Transport_Types : "+Transport_Types+";  Start_Time : "+Start_Time+"; End_Time: "+End_Time+"; Slected_Stations: "
       +request.form.getlist('mymultiselect')
       #create json file
    return render_template("index.html")

if __name__=='__main__':
    app.run()