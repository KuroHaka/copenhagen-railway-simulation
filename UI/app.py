# importing Flask and other modules
from flask import Flask, request, render_template

import json, os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

open("sample.json", "w") as outfile:
app = Flask(__name__)  #flask constructor

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])

def Run_Simulation():  # process functions
    if request.method == "POST":
       # getting input with name = fname in HTML form
       Number_of_Persons=request.form.get("Number_of_Persons")
       Number_of_Trains=request.form.get("Number_of_Trains/Carriers")
       Transport_Types=request.form.get("Switchers")
       return "The input information is, " + "Number_of_Trains: " + Number_of_Trains +"; Number_of_Persons: "+Number_of_Persons+";  Transport_Types : "+Transport_Types

       '''
       new_model_file = open(os.path.join(dirname, '../assets/model.json'), mode="w", encoding="utf-8")
        '''
       #create json file
    return render_template("index.html")

if __name__=='__main__':
    app.run()

 


 
