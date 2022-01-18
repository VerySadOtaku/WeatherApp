from enum import unique
from flask import Flask
from flask import render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

import requests


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
api_key = app.config['API_KEY']

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<City %r>' % self.city

def get_api_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    r = requests.get(url).json()
    return r


@app.route("/")
def weather_page():
    cities = City.query.all()

    weather_info = []

    for city in cities:
        record = get_api_data(city.city)
        weather = {
            'city' : city.city,
            'temperature' : record['main']['temp'],
            'description' : record['weather'][0]['description'],
            'icon' : record['weather'][0]['icon'],
        }
        weather_info.append(weather)

    return render_template('weather.html', weather_info=weather_info, cities=cities)

@app.route("/", methods=["POST"])
def add_city():
    if request.method == 'POST':
        city_name=request.form.get('city')
        city_check = get_api_data(city_name)
        print(city_check["cod"])
        if city_check["cod"] == 200:
            add_record=City(city=city_name)
            db.session.add(add_record)
            db.session.commit()
            flash(f'{city_name} has been added', 'success')
        else:
            flash(f'{city_name} does not exist', 'error')
    return redirect(url_for('weather_page'))

@app.route("/delete/<name>")
def delete_city(name):
    city_name = City.query.filter_by(city=name).first()
    db.session.delete(city_name)
    db.session.commit()
    flash(f'{city_name.city} has been deleted succesfully', 'success')
    
    return redirect(url_for('weather_page'))
