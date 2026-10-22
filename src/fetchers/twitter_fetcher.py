# Future fetcher that needs auth
from src.fetchers.base_fetcher import BaseFetcher
from src.fetchers.interfaces import AuthenticatedFetcher


class TwitterFetcher(BaseFetcher, AuthenticatedFetcher):
    """
    Fetch from Twitter API.
    
    Implements both BaseFetcher and AuthenticatedFetcher.
    """
    
    async def fetch_articles(self):
        # First authenticate
        if not await self.authenticate():
            return []
        
        # Then fetch
        ...
    
    async def authenticate(self):
        # Twitter-specific auth
        ...
