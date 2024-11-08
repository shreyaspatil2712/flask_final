

from extract import extract_data
from transform import transform_data
from load import load_to_mysql, load_to_mongodb

if __name__ == "__main__":
    # Step 1: Extract
    raw_data = extract_data()

    # Step 2: Transform
    transformed_data = transform_data(raw_data)

    # Step 3: Load to MySQL
    load_to_mysql(transformed_data)

    # Step 4: Load to MongoDB
    load_to_mongodb(transformed_data)

    print("ETL pipeline executed successfully.")
