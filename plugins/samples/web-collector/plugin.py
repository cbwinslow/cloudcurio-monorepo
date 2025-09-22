from plugins.framework.types import DataCollectionPlugin
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup

class PluginImplementation(DataCollectionPlugin):
    """Web collector plugin implementation"""
    
    def initialize(self) -> bool:
        """Initialize the web collector plugin"""
        print(f"Initializing {self.name} v{self.version}")
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Collect data from a web source"""
        url = kwargs.get('url')
        if not url:
            raise ValueError("URL is required")
        
        try:
            headers = {
                'User-Agent': self.get_config('user_agent', 'Mozilla/5.0')
            }
            
            response = requests.get(
                url, 
                headers=headers, 
                timeout=self.get_config('timeout', 30)
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            data = {
                'url': url,
                'title': soup.title.string if soup.title else 'No title',
                'links': [a.get('href') for a in soup.find_all('a', href=True)],
                'images': [img.get('src') for img in soup.find_all('img', src=True)],
                'text_content': soup.get_text()[:1000]  # Limit to first 1000 characters
            }
            
            return data
        except Exception as e:
            return {'error': str(e), 'url': url}
    
    def cleanup(self) -> None:
        """Clean up resources"""
        print(f"Cleaning up {self.name}")