import requests
import json
import os
from typing import Dict, Any, List
from grafana_api.grafana_face import GrafanaFace

class DashboardManager:
    """Manager for Grafana and OpenSearch dashboards"""
    
    def __init__(self):
        """Initialize dashboard manager with Grafana API client"""
        self.grafana_api_key = os.getenv("GRAFANA_API_KEY")
        self.grafana_host = os.getenv("GRAFANA_HOST", "localhost")
        self.grafana_port = os.getenv("GRAFANA_PORT", "3000")
        
        if self.grafana_api_key:
            self.grafana = GrafanaFace(
                auth=self.grafana_api_key,
                host=f"{self.grafana_host}:{self.grafana_port}"
            )
        else:
            self.grafana = None
    
    def create_grafana_dashboard(self, dashboard_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Grafana dashboard"""
        if not self.grafana:
            raise ValueError("Grafana API key not configured")
        
        try:
            response = self.grafana.dashboard.update_dashboard(dashboard_config)
            return response
        except Exception as e:
            raise Exception(f"Failed to create Grafana dashboard: {str(e)}")
    
    def get_grafana_dashboards(self) -> List[Dict[str, Any]]:
        """Get list of Grafana dashboards"""
        if not self.grafana:
            raise ValueError("Grafana API key not configured")
        
        try:
            dashboards = self.grafana.search.search_dashboards()
            return dashboards
        except Exception as e:
            raise Exception(f"Failed to get Grafana dashboards: {str(e)}")
    
    def create_opensearch_dashboard(self, dashboard_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create an OpenSearch dashboard"""
        opensearch_host = os.getenv("ELASTICSEARCH_HOST", "localhost")
        opensearch_port = os.getenv("ELASTICSEARCH_PORT", "9200")
        
        url = f"http://{opensearch_host}:{opensearch_port}/_dashboards/api/saved_objects/dashboard"
        
        headers = {
            "Content-Type": "application/json",
            "osd-xsrf": "true"
        }
        
        try:
            response = requests.post(url, headers=headers, json=dashboard_config)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to create OpenSearch dashboard: {str(e)}")
    
    def search_dashboards(self, query: str) -> List[Dict[str, Any]]:
        """Search for existing dashboards"""
        # This would implement dashboard search functionality
        # For now, returning empty list
        return []
    
    def load_dashboard_template(self, template_name: str) -> Dict[str, Any]:
        """Load a dashboard template by name"""
        template_path = f"./templates/dashboards/{template_name}.json"
        
        try:
            with open(template_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load dashboard template {template_name}: {str(e)}")

# Global dashboard manager instance
dashboard_manager = DashboardManager()