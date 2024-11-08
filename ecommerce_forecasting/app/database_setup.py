# database_setup.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mongoengine import connect
from config import MYSQL_URI, MONGODB_URI

# MySQL Database Connection
engine = create_engine(MYSQL_URI)
Session = sessionmaker(bind=engine)
mysql_session = Session()

# MongoDB Connection (Mongoengine)
connect(host=MONGODB_URI)
