from flask import Flask
from flask import render_template

app = Flask(__name__)  #flask instance

@app.route("/")   #url address
def hello_there(name = None):  # process functions
    return render_template(
        "index.html",
        name=name
    )

@app.route('/')
def index():
    return {
        "msg": "success",
        "data": "welcome to use flask."
    }


def user_info(u_id):
    return {
        "msg": "success",
        "data": {
            "id": u_id,
            "username": 'yuz',
            "age": 18
        }
    }

if __name__=='__main__':
    app.run()
