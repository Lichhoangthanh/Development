import os

SECRET_KEY = 'secret-key'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://username:password@std-mysql.ist.mospolytech.ru/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')