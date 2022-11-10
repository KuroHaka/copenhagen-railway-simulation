from flask import Flask  #import class flask
app=Flask(__name__)      #creat instance

@app.route('/')  #
def hello_there():
    return 'hello, World!'
