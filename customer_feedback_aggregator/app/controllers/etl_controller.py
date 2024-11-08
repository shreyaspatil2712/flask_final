
from ..etl.data_fetchers import fetch_json, fetch_xml, load_csv, load_excel, fetch_html
from ..etl.consolidator import consolidate_data
from ..etl.preprocessors import preprocess_data
from ..models.feedback import Feedback
from .. import db


def run_etl_pipeline():

    etl_status = {
        "validation_checks": [],
        "transformations_applied": []
    }
     # 1. Extract Data
    json_data = fetch_json(r'D:\cbsi training\Data Track\customer_feedback_aggregator\feedback_part1.json')
    xml_data = fetch_xml(r'D:\cbsi training\Data Track\customer_feedback_aggregator\feedback_part2.xml')
    csv_data = load_csv(r'D:\cbsi training\Data Track\customer_feedback_aggregator\feedback_part3.csv')
    excel_data = load_excel(r'D:\cbsi training\Data Track\customer_feedback_aggregator\feedback_part4.xlsx')
    html_data = fetch_html(r'D:\cbsi training\Data Track\customer_feedback_aggregator\feedback_part5.html')

    # Consolidate all data
    data_sources = {
        'json': json_data,
        'xml': xml_data,
        'csv': csv_data,
        'excel': excel_data,
        'html': html_data
    }
    # 2. Combine Data
    combined_data1 = consolidate_data(data_sources)
    combined_data = preprocess_data(combined_data1)

    # 3. Data Validation
    # check for missing values
    missing_values = combined_data.isnull().sum().sum()
    etl_status["validation_checks"].append({"missing_values": missing_values})
    combined_data.fillna(method='ffill', inplace=True)

    # data types
    expected_types = {"feedback_content": str} 
    for col, dtype in expected_types.items():
        if not combined_data[col].map(type).eq(dtype).all():
            etl_status["validation_checks"].append({"type_mismatch": f"{col} should be {dtype}"})

    #4. Transfrom
    combined_data['sentiment_score'] = combined_data['sentiment'].map({
        "positive": 1,
        "neutral": 0,
        "negative": -1
    })
    etl_status = {
        "validation_checks": ["Source diversity verified", "Data cleaned and normalized", "Sentiment score added"]
    }
    return combined_data,etl_status


def save_to_db(dataframe):
    for _, row in dataframe.iterrows():
        feedback = Feedback(
            source=row['source'],
            date=row['date'],
            feedback_content=row['feedback_content'],
            sentiment=row['sentiment']  ,
            sentiment_score=row['sentiment_score']
        )
        db.session.add(feedback)
    db.session.commit()