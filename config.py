import os

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///donation_platform.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking overhead
