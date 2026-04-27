import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/membership_inventory")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
