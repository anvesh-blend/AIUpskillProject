"""Fetch top stories from HackerNews."""

import asyncio
from datetime import datetime
from typing import Dict, List

import aiohttp

from src.models.article import Article
from src.utils.rate_limiter import RateLimiter

from src.fetchers.base_fetcher import BaseFetcher
from typing import List
import aiohttp
from src.models.article import Article

class HackerNewsFetcher(BaseFetcher):
    """
    Fetches top stories from HackerNews API.
    
    Inherits from BaseFetcher.
    Only implements source-specific logic.

    API Docs: https://github.com/HackerNews/API
    """

    # def __init__(self, storage, transformer):
    #     # self.storage = MarkdownStorage()
    #     # self.rate_limiter = RateLimiter(max_concurrent=10)
    #     # self.transformer = ArticleTransformer()
    #     self.storage = storage
    #     self.transformer = transformer
    #     self.rate_limiter = RateLimiter(max_concurrent=10)

    # BASE_URL = "https://hacker-news.firebaseio.com/v0"

    # async def fetch(self, limit: int = 30) -> List[Article]:
    #     """
    #     Fetch top stories from HackerNews.

    #     Args:
    #         limit: Number of stories to fetch (default 30)

    #     Returns:
    #         List of Article objects
    #     """
    #     print(f"📰 Fetching {limit} stories from HackerNews...")

    #     # Step 1: Get top story IDs
    #     story_ids = await self._fetch_top_story_ids()

    #     # Step 2: Fetch first N stories concurrently
    #     raw_stories = await self._fetch_stories(story_ids[:limit])

    #     # Step 3: transform to articles
    #     articles = self.transformer.transform_hackernews(raw_stories)

    #     print(f"✅ Fetched {len(articles)} HackerNews stories")
    #     return articles

    # async def _fetch_top_story_ids(self) -> List[int]:
    #     """Fetch list of top story IDs."""
    #     url = f"{self.BASE_URL}/topstories.json"

    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url) as response:
    #             story_ids = await response.json()
    #             return story_ids

    # async def _fetch_stories(self, story_ids: List[int]) -> List[Dict]:
    #     """
    #     Fetch multiple stories concurrently.

    #     This is where async shines - fetch all at once!
    #     """
    #     # Create tasks for all stories
    #     tasks = [self._fetch_story(story_id) for story_id in story_ids]

    #     # Run all tasks concurrently
    #     stories = await asyncio.gather(*tasks)

    #     # Filter out None (failed fetches)
    #     return [s for s in stories if s is not None]

    # async def _fetch_story(self, story_id: int) -> Dict:
    #     """Fetch single story with rate limiting."""
    #     url = f"{self.BASE_URL}/item/{story_id}.json"

    #     try:
    #         # Use rate limiter
    #         async with self.rate_limiter:
    #             async with aiohttp.ClientSession() as session:
    #                 async with session.get(url) as response:
    #                     return await response.json()
    #     except Exception as e:  # pylint: disable=broad-exception-caught
    #         print(f"⚠️  Failed to fetch story {story_id}: {e}")
    #         return None

    # async def fetch_and_save(self, limit: int = 30) -> List[Article]:
        # """Fetch articles and save to markdown."""
        # articles = await self.fetch(limit)

        # if articles:
        #     self.storage.save(articles, "hackernews_articles.md")

        # return articles

    async def fetch_articles(self) -> List[Article]:
        """Fetch from HackerNews API."""
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        
        async with aiohttp.ClientSession() as session:
            # Get top story IDs
            async with session.get(url) as response:
                story_ids = await response.json()
            
            # Fetch first 30 stories
            stories = []
            for story_id in story_ids[:30]:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                async with session.get(item_url) as response:
                    item = await response.json()
                    if item:
                        stories.append(item)
            
            # Transform using injected transformer
            return self.transformer.transform_hackernews(stories)
    
    def get_source_name(self) -> str:
        """Return source name."""
        return "hackernews"


# # Test it
# async def test_fetch():
#     """Quick test of fetcher."""
#     fetcher = HackerNewsFetcher()
#     articles = await fetcher.fetch(limit=5)

#     print("\n📊 Results:")
#     for article in articles:
#         print(f"  - {article.title[:50]}...")

#     return articles


# if __name__ == "__main__":
#     asyncio.run(test_fetch())