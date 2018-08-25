import os

DEBUG = os.environ.get('FLASK_DEBUG', True)
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'xxxx')

SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DATABASE_URI', 'sqlite:///songs.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False

QUERY_LIMIT = os.environ.get('QUERY_LIMIT', 100)
