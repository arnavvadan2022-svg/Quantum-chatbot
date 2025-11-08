import re
from config import Config


class QueryProcessor:
    """Process and validate user queries"""

    def __init__(self):
        self.quantum_keywords = Config.QUANTUM_KEYWORDS

    def process(self, query: str) -> str:
        """Clean and process the query"""
        # Remove extra whitespace
        query = ' '.join(query.split())

        # Remove special characters except ? and -
        query = re.sub(r'[^\w\s\?\-]', '', query)

        return query.strip()

    def is_quantum_related(self, query: str) -> bool:
        """Check if query is related to quantum topics"""
        query_lower = query.lower()

        # Check if any quantum keyword is in the query
        return any(keyword in query_lower for keyword in self.quantum_keywords)