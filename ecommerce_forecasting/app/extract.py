import pandas as pd
import xml.etree.ElementTree as ET

# Define file paths for extraction
file_paths = {
    'json': '../data/raw/ecommerce_part1.json',
    'csv': '../data/raw/ecommerce_part2.csv',
    'xml': '../data/raw/ecommerce_part3.xml',
    'excel': '../data/raw/ecommerce_part4.xlsx',
    'html': '../data/raw/ecommerce_part5.html'
}

def extract_data():
    """Extract data from multiple sources and return as a combined DataFrame."""
    
    json_data = pd.read_json(file_paths['json'])

    csv_data = pd.read_csv(file_paths['csv'])

    tree = ET.parse(file_paths['xml'])
    root = tree.getroot()
    xml_data = [{child.tag: child.text for child in record} for record in root]
    xml_data = pd.DataFrame(xml_data)

    excel_data = pd.read_excel(file_paths['excel'])

    html_data = pd.read_html(file_paths['html'])[0]  

    combined_data = pd.concat([json_data, csv_data, xml_data, excel_data, html_data], ignore_index=True)
    print("Data extracted from all sources.")
    return combined_data
