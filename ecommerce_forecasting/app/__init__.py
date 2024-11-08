from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask import render_template
from .etl import extract, transform, load
from .models import db,User,ECommerceData
from flask_migrate import Migrate
from io import BytesIO
import base64
import pandas as pd
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text

import matplotlib.pyplot as plt


login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .routes import main
    app.register_blueprint(main, url_prefix='')
    migrate = Migrate(app, db)

  
    
    with app.app_context():
        db.create_all()


    
    @app.route('/run-etl')
    def run_etl():
        
        raw_data, validation_messages = extract()
        
      
        transformed_data, transform_messages = transform(raw_data)
        validation_messages.extend(transform_messages)
        
        
        load_messages = load(transformed_data)
        validation_messages.extend(load_messages)
        
        
        return render_template('etl_result.html', messages=validation_messages, data=transformed_data.to_html())
    

    
    @app.route("/dashboard1")
    def dashboard1():
        # Fetch data from the ECommerceData table
        records = ECommerceData.query.all()

        # Convert the list of ORM objects into a list of dictionaries
        data = [record.__dict__ for record in records]
        
        # Remove any unnecessary SQLAlchemy metadata (e.g., `_sa_instance_state`)
        for item in data:
            item.pop('_sa_instance_state', None)
        
        # Create a DataFrame from the list of dictionaries
        data = pd.DataFrame(data)
        data = data.head(100)
        plots = {}

        # 1. Sales by day
        fig, ax = plt.subplots()
        data.groupby('order_date')['sales'].sum().plot(kind='line', marker='o', ax=ax)
        ax.set_title('Total Sales by  Day')
        ax.set_xlabel(' Day')
        ax.set_ylabel('Sales')
        plots['hourly_sales'] = fig_to_base64(fig)

        # 3. Sales by Hour
        fig, ax = plt.subplots()
        data.groupby('order_hour')['sales'].sum().plot(kind='line', marker='o', ax=ax)
        ax.set_title('Total Sales by Hour of Day')
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Sales')
        plots['hourly_sales'] = fig_to_base64(fig)

        # 4. Average Aging by Product
        fig, ax = plt.subplots()
        data.groupby('product')['aging'].mean().plot(kind='bar', ax=ax, color='purple')
        ax.set_title('Average Aging by Product')
        ax.set_xlabel('Product Category')
        ax.set_ylabel('Average Aging')
        plots['aging_by_product'] = fig_to_base64(fig)

        # 5. Sales by Gender
        fig, ax = plt.subplots()
        data.groupby('gender')['sales'].sum().plot(kind='bar', color=['blue', 'pink'], ax=ax)
        ax.set_title('Total Sales by Gender')
        ax.set_xlabel('Gender')
        ax.set_ylabel('Sales')
        plots['sales_by_gender'] = fig_to_base64(fig)

        # 5. Sales by Product
        fig, ax = plt.subplots()
        data.groupby('product')['sales'].sum().plot(kind='bar', ax=ax)
        ax.set_title('Total Sales by Prodcut')
        ax.set_xlabel('Gender')
        ax.set_ylabel('Sales')
        plots['sales_by_gender'] = fig_to_base64(fig)

        # 6. Sales by Customer Login Type
        fig, ax = plt.subplots()
        data.groupby('customer_login_type')['sales'].sum().plot(kind='bar', color='orange', ax=ax)
        ax.set_title('Sales by Customer Login Type')
        ax.set_xlabel('Login Type')
        ax.set_ylabel('Sales')
        plots['sales_by_login_type'] = fig_to_base64(fig)

        return render_template('dashboard.html', plots=plots)
    for rule in app.url_map.iter_rules():
       print(rule)

    return app

def fig_to_base64(fig):
    """Convert a Matplotlib figure to a base64 string for rendering in HTML."""
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')   
