#!/usr/bin/env python3

import os
import requests
import json
from typing import Dict, Any

def download_dashboard_template(url: str, filename: str, target_dir: str = "./templates/dashboards"):
    """Download a dashboard template from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Ensure target directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        # Save the template
        filepath = os.path.join(target_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            if url.endswith('.json'):
                # If it's already JSON, save as-is
                f.write(response.text)
            else:
                # If it's a GitHub repo, we might need to parse differently
                # For now, just save the raw response
                f.write(response.text)
        
        print(f"Downloaded {filename} to {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to download {filename}: {str(e)}")
        return None

def main():
    """Download dashboard templates"""
    templates = [
        {
            "name": "misp_threat_intelligence",
            "url": "https://raw.githubusercontent.com/MISP/MISP-GRAFANA/master/misp-grafana.json",
            "description": "MISP Threat Intelligence Dashboard"
        },
        {
            "name": "crowdsec_ids",
            "url": "https://raw.githubusercontent.com/GABACORREASB/CROWMOND/main/grafana/dashboards/crowdsec.json",
            "description": "CrowdSec IDS Dashboard"
        }
    ]
    
    print("Downloading dashboard templates...")
    for template in templates:
        print(f"Downloading {template['name']}...")
        download_dashboard_template(template["url"], template["name"])
    
    print("Dashboard template download complete!")

if __name__ == "__main__":
    main()