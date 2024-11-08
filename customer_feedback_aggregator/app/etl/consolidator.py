
import pandas as pd
from .preprocessors import preprocess_data

def add_source_column(dataframe, source_name):
    dataframe['source'] = source_name
    return dataframe

def consolidate_data(data_sources):
    combined_data = pd.DataFrame()
    for source_name, data in data_sources.items():
        if data is not None:
            data = add_source_column(data, source_name)
            data = preprocess_data(data)
            combined_data = pd.concat([combined_data, data], ignore_index=True)
    return combined_data
