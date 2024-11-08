
from flask import Blueprint, render_template
from flask_login import login_required, current_user
import pandas as pd
from plotly.express import bar, pie, line
from .models.feedback import Feedback

dashboard_bp = Blueprint('dashboard', __name__)
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Load data from the database
    feedback_data = Feedback.query.all()
    data = pd.DataFrame([(f.source, f.sentiment_score, f.date) for f in feedback_data],
                        columns=['Source', 'SentimentScore', 'Timestamp'])
    
    # Generate charts based on user role
    if current_user.role == 'admin':
        charts = generate_admin_charts(data)
    elif current_user.role == 'analyst':
        charts = generate_analyst_charts(data)
    else:
        charts = generate_viewer_charts(data)
        
    return render_template('dashboard.html', charts=charts)

def sentiment_trend_chart(data):
    line_chart = line(data, x='Timestamp', y='SentimentScore', title="Sentiment Over Time")
    return line_chart.to_html(full_html=False)

def feedback_source_distribution(data):
    pie_chart = pie(data, names='Source', title="Feedback Source Distribution")
    return pie_chart.to_html(full_html=False)

def average_sentiment_by_source(data):
    avg_sentiment = data.groupby('Source').SentimentScore.mean().reset_index()
    bar_chart = bar(avg_sentiment, x='Source', y='SentimentScore', title="Average Sentiment by Source")
    return bar_chart.to_html(full_html=False)

def sentiment_distribution(data):
    hist_chart = bar(data, x='SentimentScore', title="Sentiment Score Distribution")
    return hist_chart.to_html(full_html=False)

def generate_admin_charts(data):
    return {
        "sentiment_trend": sentiment_trend_chart(data),
        "feedback_source_distribution": feedback_source_distribution(data),
        "average_sentiment_by_source": average_sentiment_by_source(data),
        "sentiment_distribution": sentiment_distribution(data),
    }

def generate_analyst_charts(data):
    return {
        "sentiment_trend": sentiment_trend_chart(data),
        "average_sentiment_by_source": average_sentiment_by_source(data),
    }

def generate_viewer_charts(data):
    return {
        "sentiment_trend": sentiment_trend_chart(data),
    }
