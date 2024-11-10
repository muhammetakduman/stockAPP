from dotenv import load_dotenv
import os

load_dotenv()  # .env dosyasını yükle

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Madem!DünyayaDargındın?')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
