import feedparser
import os
from datetime import datetime
import requests

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

companies = ['GoKwik', 'Shopflo', 'Simpl', 'Razorpay Magic Checkout']
news_data = {}

try:
    for company in companies:
        url = f"https://news.google.com/rss/search?q={company.replace(' ', '+')}+checkout"
        feed = feedparser.parse(url)
        news_data[company] = [{'title': entry.title, 'link': entry.link} for entry in feed.entries[:20]]
    
    # HTML Generation
    html_content = f"<html><body style='font-family: sans-serif; padding: 20px;'>"
    html_content += "<h1>Checkout Companies News Tracker</h1>"
    html_content += f"<p>Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>"
    
    for company, articles in news_data.items():
        html_content += f"<h2>{company} (Latest {len(articles)} Articles)</h2><ul>"
        for art in articles:
            html_content += f"<li><a href='{art['link']}' target='_blank'>{art['title']}</a></li>"
        html_content += "</ul>"
        
    html_content += "</body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
except Exception as e:
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": f" Alert: News Tracker failed! Error: {str(e)}"})
    else:
        print(f"Failed to run tracker: {e}")
