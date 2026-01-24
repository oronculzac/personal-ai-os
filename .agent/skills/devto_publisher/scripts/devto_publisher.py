"""
Dev.to Publisher - Publish blog posts to Dev.to

This module creates and publishes articles to Dev.to from session logs
or weekly summaries.
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class DevToArticle:
    title: str
    body_markdown: str
    tags: List[str]
    published: bool = False
    series: Optional[str] = None
    canonical_url: Optional[str] = None


@dataclass
class PublishResult:
    success: bool
    article_id: Optional[int]
    url: Optional[str]
    error: Optional[str]


class DevToClient:
    """Client for Dev.to Forem API."""
    
    BASE_URL = "https://dev.to/api"
    
    def __init__(self, api_key: Optional[str] = None, config_path: Optional[Path] = None):
        self.api_key = api_key
        
        if not self.api_key and config_path:
            self.api_key = self._load_api_key(config_path)
        
        if not self.api_key:
            default_config = Path(".agent/config/mcp_config.json")
            if default_config.exists():
                self.api_key = self._load_api_key(default_config)
    
    def _load_api_key(self, config_path: Path) -> Optional[str]:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get("devto", {}).get("api_key")
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
    
    def test_connection(self) -> Dict:
        """Test API connection and get user info."""
        if not self.api_key:
            return {"success": False, "error": "No API key configured"}
        
        try:
            response = requests.get(f"{self.BASE_URL}/users/me", headers=self._headers())
            if response.status_code == 200:
                user = response.json()
                return {
                    "success": True,
                    "username": user.get("username"),
                    "name": user.get("name"),
                    "articles_count": user.get("articles_count", 0)
                }
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_article(self, article: DevToArticle) -> PublishResult:
        """Create a new article on Dev.to."""
        if not self.api_key:
            return PublishResult(
                success=False,
                article_id=None,
                url=None,
                error="No API key configured"
            )
        
        payload = {
            "article": {
                "title": article.title,
                "body_markdown": article.body_markdown,
                "tags": article.tags[:4],  # Dev.to allows max 4 tags
                "published": article.published
            }
        }
        
        if article.series:
            payload["article"]["series"] = article.series
        if article.canonical_url:
            payload["article"]["canonical_url"] = article.canonical_url
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/articles",
                headers=self._headers(),
                json=payload
            )
            
            if response.status_code == 201:
                data = response.json()
                return PublishResult(
                    success=True,
                    article_id=data.get("id"),
                    url=data.get("url"),
                    error=None
                )
            else:
                return PublishResult(
                    success=False,
                    article_id=None,
                    url=None,
                    error=f"API error {response.status_code}: {response.text}"
                )
        except Exception as e:
            return PublishResult(
                success=False,
                article_id=None,
                url=None,
                error=str(e)
            )
    
    def get_my_articles(self, page: int = 1, per_page: int = 10) -> List[Dict]:
        """Get list of my published articles."""
        if not self.api_key:
            return []
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/articles/me",
                headers=self._headers(),
                params={"page": page, "per_page": per_page}
            )
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def delete_article(self, article_id: int) -> bool:
        """Delete an article by ID."""
        if not self.api_key:
            return False
        
        try:
            response = requests.delete(
                f"{self.BASE_URL}/articles/{article_id}",
                headers=self._headers()
            )
            return response.status_code == 204 or response.status_code == 200
        except:
            return False


def session_log_to_article(log_path: Path, series: str = "Learning in Public") -> DevToArticle:
    """Convert a session log to a Dev.to article."""
    content = log_path.read_text(encoding='utf-8')
    
    # Extract date from filename
    date_str = log_path.stem.split("_")[0]
    
    # Extract title from content or generate one
    lines = content.split("\n")
    title = f"Learning in Public: {date_str}"
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    
    # Convert to Dev.to markdown format
    body = f"""---
title: {title}
published: false
description: Daily learning log from my Data Engineering journey
tags: learninginpublic, dataengineering, python, til
series: {series}
---

{content}

---

*This post was auto-generated from my [Learning-in-Public workflow](https://github.com/oronculzac/personal-ai-os)*
"""
    
    return DevToArticle(
        title=title,
        body_markdown=body,
        tags=["learninginpublic", "dataengineering", "python", "til"],
        published=False,  # Draft by default
        series=series
    )


def weekly_summary_to_article(summary_content: str, week_range: str) -> DevToArticle:
    """Convert a weekly summary to a Dev.to article."""
    title = f"Weekly Learning Recap: {week_range}"
    
    body = f"""---
title: {title}
published: false
description: Weekly summary of my Data Engineering learning journey
tags: learninginpublic, dataengineering, weeklyreview, progress
series: Weekly Recaps
---

{summary_content}

---

*Auto-generated by my [Personal AI OS](https://github.com/oronculzac/personal-ai-os)*
"""
    
    return DevToArticle(
        title=title,
        body_markdown=body,
        tags=["learninginpublic", "dataengineering", "weeklyreview", "progress"],
        published=False,
        series="Weekly Recaps"
    )


# CLI
if __name__ == "__main__":
    import sys
    
    client = DevToClient()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--test":
            result = client.test_connection()
            if result["success"]:
                print(f"✅ Connected to Dev.to!")
                print(f"   Username: {result['username']}")
                print(f"   Name: {result['name']}")
                print(f"   Articles: {result['articles_count']}")
            else:
                print(f"❌ Connection failed: {result['error']}")
        
        elif command == "--articles":
            articles = client.get_my_articles()
            print(f"Your articles ({len(articles)}):")
            for a in articles:
                print(f"  - [{a.get('published', False) and '✓' or '○'}] {a.get('title')}")
        
        elif command == "--publish" and len(sys.argv) > 2:
            log_path = Path(sys.argv[2])
            if log_path.exists():
                article = session_log_to_article(log_path)
                print(f"Creating article: {article.title}")
                print(f"Tags: {', '.join(article.tags)}")
                print(f"Published: {article.published}")
                print("\n--- Preview ---")
                print(article.body_markdown[:500])
                print("...")
                print("\nTo actually publish, use --publish-confirm")
            else:
                print(f"File not found: {log_path}")
        
        elif command == "--publish-confirm" and len(sys.argv) > 2:
            log_path = Path(sys.argv[2])
            if log_path.exists():
                article = session_log_to_article(log_path)
                result = client.create_article(article)
                if result.success:
                    print(f"✅ Article created!")
                    print(f"   ID: {result.article_id}")
                    print(f"   URL: {result.url}")
                else:
                    print(f"❌ Failed: {result.error}")
        
        else:
            print("Usage:")
            print("  python devto_publisher.py --test")
            print("  python devto_publisher.py --articles")
            print("  python devto_publisher.py --publish <log_file>")
            print("  python devto_publisher.py --publish-confirm <log_file>")
    else:
        result = client.test_connection()
        if result["success"]:
            print(f"✅ Dev.to connected: @{result['username']}")
        else:
            print(f"❌ {result['error']}")
