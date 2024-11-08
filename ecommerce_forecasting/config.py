from datetime import timedelta
class Config:
    SECRET_KEY =  'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ROOT2003@localhost/forecasting_db'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGODB_URI = 'mongodb://localhost:27017/forecasting_db'
