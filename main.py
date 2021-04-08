from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, session

from flask_sqlalchemy import SQLAlchemy

import random
import logging
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qr-party.db'
db = SQLAlchemy(app)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    at_party = db.Column(db.Boolean, nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name

db.create_all()

@app.route('/')
def home():
    number_of_guests = Guest.query.filter_by(at_party=True).count()
    return render_template('numberofguests.html', number_of_guests=number_of_guests)

@app.route('/signin')
def signin():
    return render_template('sign.html')

@app.route('/arrived', methods=['GET', 'POST'])
def arrived():
    if request.method == 'POST':
        name = request.form['name']
        guest = Guest(name=name, at_party=True, time_in=datetime.now())
        db.session.add(guest)
        db.session.commit()
        flash(f'You successfully signed in as {name}')
        return redirect(url_for('home'))
    return render_template('arrived.html')

@app.route('/leaving', methods=['GET', 'POST'])
def leaving():
    if request.method == 'POST':
        guest_id = request.form['name']
        guest = Guest.query.filter_by(id=guest_id).first()
        guest.at_party = False
        guest.time_out = datetime.now()
        db.session.commit()
        flash(f'Goodbye {guest.name}!')
        #session['name'] = name
        return redirect(url_for('home'))
    guests = Guest.query.filter_by(at_party=True).all()
    return render_template('leaving.html', guests=guests)

@app.route('/contact')
def contact():
    number_of_guests = 1
    return render_template('contact.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)