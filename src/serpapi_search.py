import requests
from typing import List, Dict, Optional
from config import Config


class SerpAPISearcher:
    """Search using SerpAPI for quantum-related content"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.SERPAPI_KEY
        self.base_url = "https://serpapi.com/search"

    def is_configured(self) -> bool:
        """Check if API key is configured"""
        return bool(self.api_key)

    def search(self, query: str) -> List[Dict]:
        """Search using SerpAPI"""
        if not self.is_configured():
            return []

        try:
            enhanced_query = f"{query} quantum mechanics quantum computing"

            params = {
                "q": enhanced_query,
                "api_key": self.api_key,
                "num": Config.MAX_SEARCH_RESULTS,
                "engine": "google"
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            results_data = response.json()

            results = []

            if 'organic_results' in results_data:
                for result in results_data['organic_results']:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('snippet', ''),
                        'link': result.get('link', ''),
                        'source': 'SerpAPI',
                        'position': result.get('position', 0)
                    })

            if 'knowledge_graph' in results_data:
                kg = results_data['knowledge_graph']
                results.append({
                    'title': kg.get('title', ''),
                    'snippet': kg.get('description', ''),
                    'link': kg.get('website', ''),
                    'source': 'SerpAPI-KnowledgeGraph',
                    'type': 'knowledge_graph'
                })

            return results

        except Exception as e:
            print(f"SerpAPI search error: {e}")
            return []