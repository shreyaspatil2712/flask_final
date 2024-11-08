import pandas as pd
from datetime import datetime
from .models import ECommerceData, db

def extract():
    """Extract data from multiple sources and combine into a single DataFrame with a source column."""
    msg = []
    df_json = pd.read_json('app\data\ecommerce_part1.json')
    df_json['source'] = 'json'
    
    df_csv = pd.read_csv('app\data\ecommerce_part2.csv')
    df_csv['source'] = 'csv'
    
    df_xml = pd.read_xml('app\data\ecommerce_part3.xml')
    df_xml['source'] = 'xml'
    
    df_excel = pd.read_excel('app\data\ecommerce_part4.xlsx')
    df_excel['source'] = 'excel'
    
    df_html = pd.read_html('app\data\ecommerce_part5.html')[0]  # First table in HTML file
    df_html['source'] = 'html'
    msg.append("Extracted data from 5 files (json ,xml,xlsx and html)")

 
    df_combined = pd.concat([df_json, df_csv, df_xml, df_excel, df_html], ignore_index=True)

    df_combined.dropna(inplace=True)
    return df_combined,msg

def validate(df, validation_status):
    """
    Validate data quality before transforming and add messages to validation_status list.
    """
    # non-negative sales values
    if (df['Sales'] < 0).any():
        validation_status.append("Invalid data: Sales values cannot be negative.")
    else:
        validation_status.append("Validation passed: All Sales values are non-negative.")
    
    #not null and not in the future
    if df['Order_Date'].isnull().any() or (df['Order_Date'] > datetime.now()).any():
        validation_status.append("Invalid data: Order_Date contains null values or dates in the future.")
    else:
        validation_status.append("Validation passed: Order_Date values are valid.")
    
    # Customer_Id  positive and non-null
    if df['Customer_Id'].isnull().any() or (df['Customer_Id'] <= 0).any():
        validation_status.append("Invalid data: Customer_Id must be positive and non-null.")
    else:
        validation_status.append("Validation passed: Customer_Id values are valid.")
    
    #Product_Category  non-empty
    if df['Product_Category'].isnull().any() or (df['Product_Category'] == "").any():
        validation_status.append("Invalid data: Product_Category must be non-empty.")
    else:
        validation_status.append("Validation passed: Product_Category values are valid.")
    
    #Gender  either 'Male' or 'Female'
    if not df['Gender'].isin(['Male', 'Female']).all():
        validation_status.append("Invalid data: Gender must be either 'Male' or 'Female'.")
    else:
        validation_status.append("Validation passed: Gender values are valid.")
    
    print("Data validation completed successfully.")
    return validation_status

def transform(df):
    transform_messages = []  
    # date numeric conversions
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Customer_Id'] = pd.to_numeric(df['Customer_Id'], errors='coerce')
    transform_messages.append("Converted Order_Date, Sales, and Customer_Id to appropriate types.")

    #aging in days
    df['Aging'] = (datetime.now() - df['Order_Date']).dt.days
    transform_messages.append("Calculated Aging in days.")

    #titlecase
    df['Product'] = df['Product'].str.title()
    transform_messages.append("Converted Product names to title case.")

    #normalize
    df['Sales'] *= 1.1
    transform_messages.append("Increased Sales values by 10% for normalization.")

    #lowercase
    df['Device_Type'] = df['Device_Type'].str.lower()

    #  order hour from time column
    try:
        df['Order_Hour'] = pd.to_datetime(df['Time'], format="%H:%M:%S", errors='coerce').dt.hour
    except ValueError:
        # format is variable or unknown
        df['Order_Hour'] = pd.to_datetime(df['Time'], errors='coerce').dt.hour

    return df, transform_messages


def load(df):
    ldmsg = []
    for _, row in df.iterrows():
        data_entry = ECommerceData(
            order_date=row['Order_Date'],
            time=row['Time'],
            aging=row['Aging'],
            customer_id=row['Customer_Id'],
            gender=row['Gender'],
            device_type=row['Device_Type'],
            customer_login_type=row['Customer_Login_type'],
            product_category=row['Product_Category'],
            product=row['Product'],
            sales=row['Sales'],
            order_hour=row['Order_Hour'],
            source=row['source']
        )
        db.session.add(data_entry)

    db.session.commit()
    print("Data loaded into database successfully.")
    ldmsg.append("Data loaded into database successfully.")
    return ldmsg

