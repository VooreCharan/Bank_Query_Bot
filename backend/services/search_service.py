import requests
from config import Config
import json

class SearchService:
    def __init__(self):
        self.serper_api_key = Config.SERPER_API_KEY
        self.jina_api_key = Config.JINA_API_KEY
    
    def search_web(self, query, num_results=5):
        """Search web using Serper API"""
        try:
            url = "https://google.serper.dev/search"
            
            payload = json.dumps({
                "q": query,
                "num": num_results
            })
            
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            return self._parse_serper_results(results)
        except Exception as e:
            print(f"Error in web search: {e}")
            return []
    
    def _parse_serper_results(self, results):
        """Parse Serper API results"""
        parsed_results = []
        
        # Parse organic results
        if 'organic' in results:
            for item in results['organic'][:5]:
                parsed_results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', ''),
                    'source': 'organic'
                })
        
        # Parse knowledge graph if available
        if 'knowledgeGraph' in results:
            kg = results['knowledgeGraph']
            parsed_results.insert(0, {
                'title': kg.get('title', ''),
                'snippet': kg.get('description', ''),
                'type': kg.get('type', ''),
                'source': 'knowledge_graph'
            })
        
        return parsed_results
    
    def fetch_url_content(self, url):
        """Fetch and parse URL content using Jina Reader API"""
        try:
            jina_url = f"https://r.jina.ai/{url}"
            
            headers = {
                'Authorization': f'Bearer {self.jina_api_key}',
                'X-Return-Format': 'text'
            }
            
            response = requests.get(jina_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            return response.text
        except Exception as e:
            print(f"Error fetching URL content: {e}")
            return None
    
    def search_banking_info(self, query, bank_name=None):
        """Search for banking-specific information"""
        if bank_name:
            search_query = f"{bank_name} {query}"
        else:
            search_query = f"banking {query}"
        
        return self.search_web(search_query)
    
    def get_latest_banking_updates(self, category="all"):
        """Get latest banking updates from various sources"""
        queries = {
            "loans": "home loan interest rate changes india latest",
            "rbi": "RBI latest updates policies 2025",
            "farmers": "farmer loan waiver compensation latest news",
            "insurance": "new insurance policies india 2025",
            "general": "banking sector updates india latest news"
        }
        
        query = queries.get(category, queries["general"])
        return self.search_web(query, num_results=10)
