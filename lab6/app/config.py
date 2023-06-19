import os

SECRET_KEY = 'cd99f6eb39b78d27742089f72bb2102587c30f7c22c4c97850ded91dda7e58cd'

SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://std_2082_lab4:12345678@std-mysql.ist.mospolytech.ru/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')