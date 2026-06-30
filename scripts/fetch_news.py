#!/usr/bin/env python3
"""
AI News Fetcher - Collects daily AI news from multiple premium sources
支持从多个优质新闻源收集 AI 新闻
"""

import json
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsSource:
    """Base class for news sources"""
    
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch(self) -> List[Dict]:
        """Fetch news from source"""
        raise NotImplementedError


class HackerNewsSource(NewsSource):
    """Fetch from Hacker News"""
    
    def __init__(self):
        super().__init__("Hacker News", "Technology & Startups")
    
    def fetch(self) -> List[Dict]:
        try:
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(url, timeout=10)
            top_stories = response.json()[:30]
            
            news_list = []
            for story_id in top_stories[:5]:  # Get top 5 stories
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=10)
                story = story_response.json()
                
                if story.get('type') == 'story' and 'title' in story:
                    news_list.append({
                        'title': story.get('title'),
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'source': self.name,
                        'category': self.category,
                        'timestamp': datetime.utcfromtimestamp(story.get('time', 0)).isoformat()
                    })
            
            logger.info(f"✓ Fetched {len(news_list)} stories from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


class ArXivSource(NewsSource):
    """Fetch latest AI papers from ArXiv"""
    
    def __init__(self):
        super().__init__("ArXiv", "AI Research & Papers")
    
    def fetch(self) -> List[Dict]:
        try:
            # Search for AI/ML papers from last 7 days
            base_url = "http://export.arxiv.org/api/query?"
            query = "cat:cs.AI OR cat:cs.LG OR cat:cs.CL"
            params = {
                'search_query': query,
                'start': 0,
                'max_results': 5,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:5]:
                news_list.append({
                    'title': entry.title.replace('\n', ' '),
                    'url': entry.id,
                    'summary': entry.summary.replace('\n', ' ')[:200],
                    'source': self.name,
                    'category': self.category,
                    'timestamp': entry.published
                })
            
            logger.info(f"✓ Fetched {len(news_list)} papers from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


class TechCrunchSource(NewsSource):
    """Fetch from TechCrunch RSS"""
    
    def __init__(self):
        super().__init__("TechCrunch", "Tech Startups & Products")
    
    def fetch(self) -> List[Dict]:
        try:
            url = "https://techcrunch.com/feed/"
            response = requests.get(url, timeout=10, headers=self.headers)
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:5]:
                # Filter for AI-related content
                title_lower = entry.title.lower()
                summary_lower = entry.get('summary', '').lower()
                if any(keyword in title_lower or keyword in summary_lower 
                       for keyword in ['ai', 'llm', 'artificial intelligence', 'machine learning', 'gpt']):
                    news_list.append({
                        'title': entry.title,
                        'url': entry.link,
                        'summary': entry.get('summary', '')[:200],
                        'source': self.name,
                        'category': self.category,
                        'timestamp': entry.get('published', '')
                    })
            
            logger.info(f"✓ Fetched {len(news_list)} articles from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


class ProductHuntSource(NewsSource):
    """Fetch from Product Hunt API"""
    
    def __init__(self):
        super().__init__("Product Hunt", "New AI Products & Tools")
    
    def fetch(self) -> List[Dict]:
        try:
            url = "https://www.producthunt.com/feed"
            response = requests.get(url, timeout=10, headers=self.headers)
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:5]:
                title_lower = entry.title.lower()
                if any(keyword in title_lower 
                       for keyword in ['ai', 'llm', 'ml', 'neural', 'automation']):
                    news_list.append({
                        'title': entry.title,
                        'url': entry.link,
                        'source': self.name,
                        'category': self.category,
                        'timestamp': entry.get('published', '')
                    })
            
            logger.info(f"✓ Fetched {len(news_list)} products from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


class TowardsDataScienceSource(NewsSource):
    """Fetch from Towards Data Science (Medium)"""
    
    def __init__(self):
        super().__init__("Towards Data Science", "AI Technical Articles")
    
    def fetch(self) -> List[Dict]:
        try:
            url = "https://towardsdatascience.com/feed"
            response = requests.get(url, timeout=10, headers=self.headers)
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:5]:
                news_list.append({
                    'title': entry.title,
                    'url': entry.link,
                    'summary': entry.get('summary', '')[:200],
                    'source': self.name,
                    'category': self.category,
                    'timestamp': entry.get('published', '')
                })
            
            logger.info(f"✓ Fetched {len(news_list)} articles from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


class DeepLearningAISource(NewsSource):
    """Fetch from Deeplearning.AI (created by Andrew Ng)"""
    
    def __init__(self):
        super().__init__("Deeplearning.AI", "AI Education & Insights")
    
    def fetch(self) -> List[Dict]:
        try:
            url = "https://www.deeplearning.ai/blog/feed/"
            response = requests.get(url, timeout=10, headers=self.headers)
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:5]:
                news_list.append({
                    'title': entry.title,
                    'url': entry.link,
                    'summary': entry.get('summary', '')[:200],
                    'source': self.name,
                    'category': self.category,
                    'timestamp': entry.get('published', '')
                })
            
            logger.info(f"✓ Fetched {len(news_list)} articles from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


class OpenAIBlogSource(NewsSource):
    """Fetch from OpenAI Blog"""
    
    def __init__(self):
        super().__init__("OpenAI Blog", "OpenAI News & Updates")
    
    def fetch(self) -> List[Dict]:
        try:
            url = "https://openai.com/blog/feed/"
            response = requests.get(url, timeout=10, headers=self.headers)
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:3]:
                news_list.append({
                    'title': entry.title,
                    'url': entry.link,
                    'summary': entry.get('summary', '')[:200],
                    'source': self.name,
                    'category': self.category,
                    'timestamp': entry.get('published', '')
                })
            
            logger.info(f"✓ Fetched {len(news_list)} articles from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


class GoogleAIBlogSource(NewsSource):
    """Fetch from Google AI Blog"""
    
    def __init__(self):
        super().__init__("Google AI", "Google AI Research & Products")
    
    def fetch(self) -> List[Dict]:
        try:
            url = "https://ai.googleblog.com/feeds/posts/default?alt=rss"
            response = requests.get(url, timeout=10, headers=self.headers)
            feed = feedparser.parse(response.content)
            
            news_list = []
            for entry in feed.entries[:3]:
                news_list.append({
                    'title': entry.title,
                    'url': entry.link,
                    'summary': entry.get('summary', '')[:200],
                    'source': self.name,
                    'category': self.category,
                    'timestamp': entry.get('published', '')
                })
            
            logger.info(f"✓ Fetched {len(news_list)} articles from {self.name}")
            return news_list
        except Exception as e:
            logger.error(f"✗ Error fetching from {self.name}: {str(e)}")
            return []


def fetch_all_news() -> List[Dict]:
    """Fetch news from all sources"""
    logger.info("=" * 60)
    logger.info("🤖 Starting AI News Collection")
    logger.info("=" * 60)
    
    sources = [
        HackerNewsSource(),
        ArXivSource(),
        TechCrunchSource(),
        ProductHuntSource(),
        TowardsDataScienceSource(),
        DeepLearningAISource(),
        OpenAIBlogSource(),
        GoogleAIBlogSource(),
    ]
    
    all_news = []
    for source in sources:
        try:
            news = source.fetch()
            all_news.extend(news)
        except Exception as e:
            logger.error(f"Error with {source.name}: {str(e)}")
    
    logger.info("=" * 60)
    logger.info(f"✓ Total {len(all_news)} news items collected")
    logger.info("=" * 60)
    
    return all_news


def save_news(news: List[Dict]) -> None:
    """Save news to JSON file"""
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'news/{today}.json'
    
    data = {
        'date': today,
        'timestamp': datetime.now().isoformat(),
        'total_count': len(news),
        'news': news
    }
    
    try:
        import os
        os.makedirs('news', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"✓ News saved to {filename}")
    except Exception as e:
        logger.error(f"✗ Error saving news: {str(e)}")


if __name__ == '__main__':
    news = fetch_all_news()
    save_news(news)
