import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://user:password@database_endpoint:3306/database_name'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
