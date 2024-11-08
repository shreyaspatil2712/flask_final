# load.py

from models.mysql_models import EcommerceData as MySQLData
from models.mongodb_models import EcommerceData as MongoData
from database_setup import mysql_session
import pandas as pd

def load_to_mysql(data: pd.DataFrame):
    """Load data into MySQL database."""
    for _, row in data.iterrows():
        record = MySQLData(
            order_date=row['Order_Date'],
            time=row['Time'],
            aging=row['Aging'],
            customer_id=row['Customer_Id'],
            gender=row['Gender'],
            device_type=row['Device_Type'],
            customer_login_type=row['Customer_Login_type'],
            product_category=row['Product_Category'],
            product=row['Product'],
            sales=row['Sales']
        )
        mysql_session.add(record)
    mysql_session.commit()
    print("Data loaded into MySQL.")

def load_to_mongodb(data: pd.DataFrame):
    """Load data into MongoDB database."""
    for _, row in data.iterrows():
        record = MongoData(
            order_date=row['Order_Date'],
            time=row['Time'],
            aging=row['Aging'],
            customer_id=row['Customer_Id'],
            gender=row['Gender'],
            device_type=row['Device_Type'],
            customer_login_type=row['Customer_Login_type'],
            product_category=row['Product_Category'],
            product=row['Product'],
            sales=row['Sales']
        )
        record.save()
    print("Data loaded into MongoDB.")
