from googleapiclient.discovery import build
from typing import List, Dict, Optional
from config import Config


class GoogleSearcher:
    """Search using Google Custom Search API"""

    def __init__(self, api_key: Optional[str] = None, cse_id: Optional[str] = None):
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.cse_id = cse_id or Config.GOOGLE_CSE_ID

    def is_configured(self) -> bool:
        """Check if API credentials are configured"""
        return bool(self.api_key and self.cse_id)

    def search(self, query: str) -> List[Dict]:
        """Search using Google Custom Search"""
        if not self.is_configured():
            return []

        try:
            service = build("customsearch", "v1", developerKey=self.api_key)

            enhanced_query = f"{query} quantum computing quantum mechanics"

            result = service.cse().list(
                q=enhanced_query,
                cx=self.cse_id,
                num=Config.MAX_SEARCH_RESULTS
            ).execute()

            results = []

            if 'items' in result:
                for item in result['items']:
                    results.append({
                        'title': item.get('title', ''),
                        'snippet': item.get('snippet', ''),
                        'link': item.get('link', ''),
                        'source': 'Google'
                    })

            return results

        except Exception as e:
            print(f"Google search error: {e}")
            return []