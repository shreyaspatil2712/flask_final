import pandas as pd

def transform_data(data):
    """Transform the extracted data."""
    #duplicates
    data = data.drop_duplicates()
    
    # missing values
    data['Aging'] = data['Aging'].fillna(data['Aging'].median())
    data['Sales'] = data['Sales'].fillna(0)

    # datetime formats
    data['Order_Date'] = pd.to_datetime(data['Order_Date'], errors='coerce')
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S', errors='coerce').dt.time

    #categorical 
    data['Gender'] = data['Gender'].fillna('Unknown')
    data['Device_Type'] = data['Device_Type'].fillna('Unknown')
    data['Customer_Login_type'] = data['Customer_Login_type'].fillna('Guest')
    data['Product_Category'] = data['Product_Category'].str.title()
    data['Product'] = data['Product'].str.title()

    # numeric
    data = data[data['Customer_Id'].apply(lambda x: str(x).isdigit())]
    data['Customer_Id'] = data['Customer_Id'].astype(int)

    print("Data transformed with cleaning and standardization.")
    return data
