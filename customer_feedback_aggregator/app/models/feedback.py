
from .. import db
from sqlalchemy import Column, Integer, String, Date, Text,Float

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    date = Column(Date)
    feedback_content = Column(Text)
    sentiment = Column(String(20))
    sentiment_score = Column(Float) 

    def __init__(self, source, date, feedback_content, sentiment,sentiment_score ):
        self.source = source
        self.date = date
        self.feedback_content = feedback_content
        self.sentiment = sentiment
        self.sentiment_score = sentiment_score 
