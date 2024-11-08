from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class ECommerceData(db.Model):
    __tablename__ = 'ecommerce_data'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    order_hour = db.Column(db.Time, nullable=False)
    aging = db.Column(db.Float)
    customer_id = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    device_type = db.Column(db.String(50))
    customer_login_type = db.Column(db.String(50))
    product_category = db.Column(db.String(100))
    product = db.Column(db.String(100))
    sales = db.Column(db.Float)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
