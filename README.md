# GoKwik AI GTM Technical Assignment

## How to run it and what runs when
- **Data Analysis (`analysis.py`)**: Before running, place `orders.csv` in the root folder. Run locally with `python analysis.py` to get the COD return rates and anomaly report.
- **News Tracker (`tracker.py`)**: Fetches news from Google News RSS and updates `index.html`. 
- **Automation**: A GitHub Action runs `tracker.py` daily at 2:00 AM UTC. It commits the updated `index.html` back to the main branch automatically. GitHub Pages instantly serves the updated HTML file.

## What will break first, and how I would find out
Google News RSS structure might change or block the automated requests, resulting in empty data. I have set up a `try-except` block in `tracker.py` that catches any failure and fires an alert to a Discord Webhook, notifying me immediately without anyone checking the logs.

## What I would build next with two more days
1. Integrate an LLM API (like Groq or Gemini) to summarize the news articles rather than just displaying titles.
2. Use a database (like Supabase free tier) instead of committing to an HTML file to track exact article history and avoid overlaps over months.
