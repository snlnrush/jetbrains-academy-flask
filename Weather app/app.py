from flask import Flask, render_template, flash
from flask import request
from flask import redirect, url_for
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
import sys
import requests


app = Flask(__name__)

DB_NAME = 'weather'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
API_WEATHER_KEY = '9abb125a77d52b47d5d488305f45395d'
API_OPEN_WEATHER = 'https://api.openweathermap.org/data/2.5/weather'

db = SQLAlchemy(app)


class City(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    def __repr__(self):
        return 'DataBase for Flask project'


db.create_all()

# with open('api_weather_key.txt', 'r') as file:
#     api_weather_key = file.readline().strip()


def request_weather(city_name: str) -> dict:
    params = {'q': city_name, 'appid': API_WEATHER_KEY}
    response = requests.get(API_OPEN_WEATHER, params=params)
    return response.json()


@app.route('/delete/<city_name>', methods=['GET', 'POST'])
def delete(city_name):
    city = City.query.filter_by(name=city_name.strip()).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        city_name = request.form['city_name']
        try:
            response_json = request_weather(city_name)
            if response_json['cod'] == '404':
                flash("The city doesn't exist!")
                return redirect('/')

            cities = City.query.all()
            for city in cities:
                if city_name == city.name:
                    flash('The city has already been added to the list!')
                    return redirect('/')

            city = City(name=city_name)
            db.session.add(city)
            db.session.commit()
        except:
            print('Ошибка добавления в БД')
        return redirect(url_for('index'))

    if request.method == 'GET':
        dict_with_weather_info = {}
        cities = City.query.all()
        for city in cities:
            city_name = city.name
            response_json = request_weather(city_name)
            if response_json['cod'] == 200:
                cur_temp_cel = int(response_json['main']['temp']) - 273
                cur_city_name = response_json['name']
                cur_weather = response_json['weather'][0]['main']
                dict_with_weather_info[city_name] = {'city_name': cur_city_name, 'temp_cel': cur_temp_cel, 'weather': cur_weather}
        return render_template('index.html', weather=dict_with_weather_info)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
