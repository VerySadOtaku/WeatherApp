from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.flaskenv'))

class Config():
    DEBUG = True
    TESTING = True
    FLASK_ENV='DEVELOPMENT'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///weather.db'
    API_KEY='d9b77dbc24c72a921cdca2e8a927c7d7'
    SECRET_KEY='very secret'