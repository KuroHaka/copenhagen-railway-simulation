# importing Flask and other modules
from flask import Flask, request, render_template

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
    return render_template("index.html")

if __name__=='__main__':
    app.run()

 


 
