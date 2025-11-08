import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
from config import Config


class ArxivSearcher:
    """Search arXiv for quantum mechanics and quantum computing papers"""

    def __init__(self):
        self.max_results = Config.ARXIV_MAX_RESULTS
        self.base_url = "http://export.arxiv.org/api/query"

    def search(self, query: str) -> List[Dict]:
        """Search arXiv for papers related to the query"""
        try:
            # Enhance query with quantum-specific terms
            enhanced_query = f'all:{query} AND (cat:quant-ph OR cat:cond-mat.mes-hall)'

            params = {
                'search_query': enhanced_query,
                'start': 0,
                'max_results': self.max_results,
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            results = self._parse_arxiv_response(response.text)
            return results

        except Exception as e:
            print(f"arXiv search error: {e}")
            return []

    def _parse_arxiv_response(self, xml_text: str) -> List[Dict]:
        """Parse arXiv API XML response"""
        results = []

        try:
            root = ET.fromstring(xml_text)

            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }

            for entry in root.findall('atom:entry', ns):
                try:
                    title_elem = entry.find('atom:title', ns)
                    title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else 'No title'

                    summary_elem = entry.find('atom:summary', ns)
                    summary = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None else 'No summary'

                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name_elem = author.find('atom:name', ns)
                        if name_elem is not None:
                            authors.append(name_elem.text.strip())

                    link_elem = entry.find('atom:id', ns)
                    link = link_elem.text.strip() if link_elem is not None else ''

                    published_elem = entry.find('atom:published', ns)
                    published = published_elem.text[:10] if published_elem is not None else ''

                    pdf_url = link.replace('abs', 'pdf') + '.pdf' if link else ''

                    results.append({
                        'title': title,
                        'summary': summary,
                        'authors': authors,
                        'published': published,
                        'link': link,
                        'pdf_url': pdf_url,
                        'source': 'arXiv'
                    })

                except Exception as e:
                    print(f"Error parsing entry: {e}")
                    continue

            return results

        except Exception as e:
            print(f"Error parsing arXiv XML: {e}")
            return []