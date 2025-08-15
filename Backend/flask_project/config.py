from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///mydatabase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "shark/uploads"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes = 15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days = 7)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/token/refresh"
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_COOKIE_NAME = "mytypingApp_token_cookie"
    JWT_REFRESH_COOKIE_NAME = "my_token_cookie"
    SECRET_KEY = os.getenv("SECRET_KEY")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    FROM_NAME = os.getenv("FROM_NAME")
