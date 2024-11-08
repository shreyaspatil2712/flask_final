import pandas as pd
import os

RAW_DATA_PATH = "../data/raw/"

file_paths = [
    f"{RAW_DATA_PATH}ecommerce_part1.json",
    f"{RAW_DATA_PATH}ecommerce_part2.csv",
    f"{RAW_DATA_PATH}ecommerce_part3.xml",
    f"{RAW_DATA_PATH}ecommerce_part4.xlsx",
    f"{RAW_DATA_PATH}ecommerce_part5.html"
]

def validate_and_integrate_data(file_paths):
    integrated_data = pd.DataFrame()

    for file_path in file_paths:
        try:
        
            if file_path.endswith(".json"):
                data = pd.read_json(file_path)
            elif file_path.endswith(".csv"):
                data = pd.read_csv(file_path)
            elif file_path.endswith(".xml"):
                data = pd.read_xml(file_path)
            elif file_path.endswith(".xlsx"):
                data = pd.read_excel(file_path)
            elif file_path.endswith(".html"):
                data = pd.read_html(file_path)[0]  
            else:
                raise ValueError("Unsupported file format.")

            # Basic Validation
            required_columns = ["Order_Date", "Time", "Aging", "Customer_Id", "Gender",
                                "Device_Type", "Customer_Login_type", "Product_Category",
                                "Product", "Sales"]

            if not all(column in data.columns for column in required_columns):
                print(f"Skipping {file_path}: Missing required columns.")
                continue

            # Data Cleaning:
            data.drop_duplicates(inplace=True)
            data.fillna({'Aging': data['Aging'].median(), 'Sales': data['Sales'].mean()}, inplace=True)

          
            integrated_data = pd.concat([integrated_data, data], ignore_index=True)
            print(f"Data from {file_path} validated and integrated.")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    
    integrated_data.to_csv(f"{RAW_DATA_PATH}integrated_data.csv", index=False)
    print("All data integrated successfully.")


validate_and_integrate_data(file_paths)
