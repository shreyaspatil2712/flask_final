from bs4 import BeautifulSoup
import pandas as pd


from bs4 import BeautifulSoup
import pandas as pd


def fetch_json(file_path):
    try:
        return pd.read_json(file_path, orient="records")
    except ValueError as e:
        print(f"Failed to fetch JSON data: {e}")
        return None

def fetch_xml(file_path):
    try:
        from lxml import etree
        tree = etree.parse(file_path)
        root = tree.getroot()
        
        data = []
        for feedback in root.findall("Feedback"):
            entry = {element.tag: element.text for element in feedback}
            data.append(entry)
        
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Failed to fetch XML data: {e}")
        return None

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Failed to load CSV data: {e}")
        return None

def load_excel(file_path):
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError as e:
        print(f"Failed to load Excel data: {e}")
        return None

def fetch_html(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            soup = BeautifulSoup(file, 'html.parser')
            feedback_elements = soup.select("div.feedback_content")  # Adjust selector as per HTML structure
            data = {"feedback_content": [element.text for element in feedback_elements]}
            return pd.DataFrame(data)
    except Exception as e:
        print(f"Failed to fetch HTML data: {e}")
        return None
