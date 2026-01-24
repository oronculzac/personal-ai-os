import os
import datetime
import feedparser
import requests
import re
from pytrends.request import TrendReq
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
CONFIG = {
    "trends_keywords": ["Artificial Intelligence", "Machine Learning", "Generative AI", "LLM", "OpenAI"],
    "rss_feeds": [
        {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
        {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
        {"name": "Reddit r/ArtificialIntelligence", "url": "https://www.reddit.com/r/ArtificialInteligence/.rss"},
        {"name": "Reddit r/LocalLLaMA", "url": "https://www.reddit.com/r/LocalLLaMA/.rss"}
    ],
    "output_dir": "vault/Areas/AI/Reports"
}

# Categorization Keywords
CATEGORIES = {
    "🧠 Models & Research": ["llm", "gpt", "model", "paper", "research", "transformer", "neural", "deepmind", "anthropic", "llama", "inference", "training"],
    "💼 Business & Funding": ["raise", "funding", "startup", "acquisition", "shares", "stock", "ipo", "invest", "venture", "valuation", "billion"],
    "⚖️ Regulation & Ethics": ["lawsuit", "ban", "regulation", "policy", "safety", "crime", "fake", "copyright", "congress", "eu", "compliance"],
    "🛠️ Tools & Apps": ["tool", "app", "extension", "plugin", "update", "feature", "copilot", "chatgpt", "gemini", "claude", "browser"],
    "🌐 General": [] # Fallback
}

def categorize_item(title, summary):
    """Categorizes an item based on keywords in title and summary."""
    text = (title + " " + summary).lower()
    
    for category, keywords in CATEGORIES.items():
        if category == "🌐 General": continue
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                return category
    
    return "🌐 General"

def get_google_trends():
    """Fetches trending related queries for configured keywords."""
    print("📈 Fetching Google Trends...")
    trends_data = {}
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        # Using a broader timeframe or related queries
        pytrends.build_payload(CONFIG["trends_keywords"], cat=0, timeframe='now 7-d', geo='', gprop='')
        related_queries = pytrends.related_queries()
        
        for keyword, data in related_queries.items():
            if data['top'] is not None:
                trends_data[keyword] = data['top'].head(3)['query'].tolist()
            else:
                trends_data[keyword] = []
                
    except Exception as e:
        print(f"⚠️ Error fetching Google Trends: {e}")
        trends_data["Error"] = [str(e)]
        
    return trends_data

def get_rss_feed(source):
    """Fetches and parses an RSS feed."""
    print(f"📰 Fetching {source['name']}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(source['url'], headers=headers, timeout=10)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        
        items = []
        for entry in feed.entries[:5]: # Top 5 items
            title = entry.title
            link = entry.link
            # Get summary, remove html tags roughly
            raw_summary = entry.get("summary", entry.get("description", ""))
            clean_summary = re.sub('<[^<]+?>', '', raw_summary)[:200] + "..."
            
            category = categorize_item(title, clean_summary)
            
            items.append({
                "title": title,
                "link": link,
                "summary": clean_summary,
                "category": category,
                "source": source['name']
            })
        return items
        
    except Exception as e:
        print(f"⚠️ Error fetching {source['name']}: {e}")
        return []

def generate_markdown(trends_data, all_news_items):
    """Generates the Markdown report."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H:%M")
    
    base_path = os.getcwd()
    output_dir = os.path.join(base_path, CONFIG["output_dir"])
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{today}-AI-Trends.md"
    filepath = os.path.join(output_dir, filename)
    
    lines = []
    lines.append(f"# 🤖 AI Research Report - {today}")
    lines.append(f"Generated at: {timestamp}")
    lines.append("")
    
    # 2. News by Category
    
    # Group by category
    categorized_news = {cat: [] for cat in CATEGORIES.keys()}
    for item in all_news_items:
        categorized_news[item['category']].append(item)
        
    lines.append("## 📰 Latest News & Updates")
    
    for category, items in categorized_news.items():
        if not items: continue
        
        lines.append(f"### {category}")
        for item in items:
            lines.append(f"#### [{item['title']}]({item['link']})")
            lines.append(f"> {item['summary']}")
            lines.append(f"> *Source: {item['source']}*")
            lines.append("")
            
    # 1. Trends at bottom or top? Let's put at bottom as "Search Interest"
    lines.append("## 📈 Search Trends (Last 7 Days)")
    if "Error" in trends_data:
        lines.append(f"> ⚠️ Failed to fetch trends: {trends_data['Error'][0]}")
    else:
        # Format as a table or list
        for keyword, queries in trends_data.items():
            if queries:
                q_str = ", ".join([f"`{q}`" for q in queries])
                lines.append(f"- **{keyword}**: {q_str}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"✅ Report generated: {filepath}")
    return filepath

def main():
    print("🚀 Starting AI Researcher (Categorized)...")
    
    # 1. Fetch Trends
    trends_data = get_google_trends()
    
    # 2. Fetch RSS Feeds
    all_news_items = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_source = {executor.submit(get_rss_feed, source): source for source in CONFIG["rss_feeds"]}
        for future in as_completed(future_to_source):
            items = future.result()
            all_news_items.extend(items)
            
    # 3. Generate Report
    generate_markdown(trends_data, all_news_items)
    print("✨ Research complete!")

if __name__ == "__main__":
    main()
