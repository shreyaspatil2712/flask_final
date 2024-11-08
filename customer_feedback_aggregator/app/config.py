
from datetime import timedelta


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PROTECTION = 'strong'
    REMEMBER_COOKIE_DURATION = timedelta(days=1)

class MySQLConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:ROOT2003@localhost/feedback"

class SQLiteConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///feedback.db"

def get_config():
    return SQLiteConfig
