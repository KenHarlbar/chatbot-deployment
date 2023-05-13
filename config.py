from os import getenv
from dotenv import load_dotenv

load_dotenv('./env')


class Config:
    DEBUG = False
    SECRET_KEY = getenv('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = getenv('WTF_CSRF_SECRET_KEY')