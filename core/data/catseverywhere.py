import os
from flask import request, redirect
from flask import Flask, render_template
from flask import g
import sqlite3
from random import randint

app = Flask(__name__)

email_addresses = []

@app.before_request
def before_request():
    g.db = sqlite3.connect("emails.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    g.db.execute("INSERT INTO email_addresses VALUES (?)", [email])
    g.db.commit()
    return redirect('/')

@app.route('/emails.html')
def emails():
    email_addresses = g.db.execute("SELECT email from email_addresses").fetchall()
    return render_template('emails.html', email_addresses=email_addresses)

@app.route('/')
def hello_world():
    name = "Cats Everywhere"
    number = randint(0,300)
    print number
    return render_template('index.html', name=name, number=number)
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
