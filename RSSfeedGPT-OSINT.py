import feedparser
import openai
import requests
import time
import numpy as np
from collections import defaultdict
from difflib import SequenceMatcher

# OpenAI API Key (Replace with your own API key)
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# List of RSS feeds
RSS_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.npr.org/rss/rss.php?id=1004",
    "https://www.theguardian.com/world/rss",
    "https://www.ft.com/rss/world",
    "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "https://globalnews.ca/feed/",
    "https://www.cbc.ca/cmlink/rss-world",
    "https://www.scmp.com/rss/91/feed",
    "https://www.japantimes.co.jp/feed/",
    "https://www.euronews.com/rss?level=theme&name=news"
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Function to fetch and parse RSS feeds
def fetch_rss_feeds():
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            response = requests.get(feed_url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                if not feed.entries:
                    print(f"Warning: No entries found in {feed_url}")
                
                # Fetch only the 3 most recent articles per feed
                for entry in feed.entries[:3]:
                    articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.get("summary", "No summary available."),
                        "published": entry.get("published", "Unknown date")
                    })
            else:
                print(f"Error fetching {feed_url}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Failed to fetch {feed_url}: {e}")
    print(f"Fetched {len(articles)} articles.")
    return articles

# Function to get OpenAI embeddings
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002", 
        input=text
    )
    return np.array(response.data[0].embedding)

# Function to find similar articles
def find_similar_articles(articles, threshold=0.85):
    embeddings = {}
    merged_articles = []
    
    for article in articles:
        embeddings[article['title']] = get_embedding(article['summary'])
    
    used = set()
    for i, article in enumerate(articles):
        if article['title'] in used:
            continue
        
        similar_group = [article]
        used.add(article['title'])
        
        for j, other_article in enumerate(articles):
            if i != j and other_article['title'] not in used:
                similarity = np.dot(embeddings[article['title']], embeddings[other_article['title']])
                if similarity > threshold:
                    similar_group.append(other_article)
                    used.add(other_article['title'])
        
        merged_text = "\n\n".join([a['summary'] for a in similar_group])
        merged_articles.append({
            "title": article['title'],
            "link": article['link'],
            "summary": merged_text
        })
    
    return merged_articles

# Function to summarize text using OpenAI
def summarize_text(text):
    if not text.strip():
        return "No content available for summarization."
    prompt = f"Summarize this news in 2 sentences:\n{text}"
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes news articles succinctly."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Function to create structured intelligence briefing
def generate_briefing_file(articles, filename="intelligence_briefing.txt"):
    if not articles:
        print("No articles to write to the briefing file.")
        return
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Intelligence Briefing Report\n" + "="*40 + "\n\n")
        for article in articles:
            f.write(f"- **Title**: {article['title']}\n")
            f.write(f"  **Summary**: {article['summary']}\n")
            f.write(f"  **Sources**: {article['link']}\n\n")
    print(f"Briefing file saved as {filename}")

# Main Execution
if __name__ == "__main__":
    print("Fetching RSS feeds...")
    raw_articles = fetch_rss_feeds()
    
    if not raw_articles:
        print("No articles fetched. Exiting...")
    else:
        print("Finding similar articles...")
        merged_articles = find_similar_articles(raw_articles)
        
        print("Summarizing articles...")
        for article in merged_articles:
            article['summary'] = summarize_text(article['summary'])
        
        print("Generating intelligence briefing...")
        generate_briefing_file(merged_articles)