from flask import Flask
from flask import render_template

app = Flask(__name__)  #flask instance

@app.route("/")   #url address
def hello_there(name = None):  # process functions
    return render_template(
        "index.html",
        name=name
    )

if __name__=='__main__':
    app.run()
