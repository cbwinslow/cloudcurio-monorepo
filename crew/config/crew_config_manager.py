import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class CrewConfigManager:
    """Manages loading and accessing crew configurations from JSON files"""
    
    def __init__(self, config_dir: str = "crew/config"):
        self.config_dir = Path(config_dir)
        self.configs = {}
        self.load_all_configs()
    
    def load_all_configs(self):
        """Load all configuration files from the config directory"""
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Configuration directory {self.config_dir} does not exist")
        
        for config_file in self.config_dir.glob("*.json"):
            self.load_config_from_file(config_file)
    
    def load_config_from_file(self, file_path: Path):
        """Load a single configuration file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Add all configurations from this file to our configs
            for crew_name, crew_config in data.items():
                self.configs[crew_name] = crew_config
    
    def get_config(self, crew_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific crew configuration by name"""
        return self.configs.get(crew_name)
    
    def get_all_crew_names(self) -> list:
        """Get a list of all available crew names"""
        return list(self.configs.keys())
    
    def validate_config(self, crew_name: str) -> bool:
        """Validate if a crew configuration is properly structured"""
        config = self.get_config(crew_name)
        if not config:
            return False
        
        # Check for required fields
        required_fields = ["name", "description", "agents", "tasks", "process"]
        for field in required_fields:
            if field not in config:
                return False
        
        # Check agents
        if not isinstance(config["agents"], list) or len(config["agents"]) == 0:
            return False
        
        # Check tasks
        if not isinstance(config["tasks"], list) or len(config["tasks"]) == 0:
            return False
        
        return True

# Global instance for easy access
config_manager = CrewConfigManager()