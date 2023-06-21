import os

SECRET_KEY = 'secret-key'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://std_1865_2023lab6:12345678@std-mysql.ist.mospolytech.ru/std_1865_2023lab6'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')