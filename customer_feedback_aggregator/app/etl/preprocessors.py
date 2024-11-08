
import pandas as pd

def preprocess_data(dataframe):
    # Standardize column names
    dataframe.columns = dataframe.columns.str.lower().str.replace(' ', '_')

    # Remove duplicates
    dataframe.drop_duplicates(inplace=True)

    # Fill NaN values with a default value
    dataframe.fillna({
        'feedback_content': 'No content',   # Replace NaN in feedback_content
        'sentiment': 'Unknown',    
        'sentiment_score': '0',         # Replace NaN in sentiment
        'date': pd.to_datetime('1970-01-01')  # Replace NaN in date with a default date
    }, inplace=True)

    # Convert 'date' column to datetime, if it exists
    if 'date' in dataframe.columns:
        dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')

    return dataframe
