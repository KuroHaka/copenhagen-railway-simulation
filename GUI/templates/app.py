from flask import Flask
from flask import render_template

app = Flask(__name__)  #flask instance


@app.route('/login1',methods=['GET', 'POST'])
def login1():
    return render_template('login1.html')
   


if __name__=='__main__':
    app.run()
