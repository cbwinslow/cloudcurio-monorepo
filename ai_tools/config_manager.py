"""
Configuration Manager for AI Agents and Providers

This module provides functionality to store, retrieve, and manage
configuration for AI agents with secure credential storage.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from .ai_provider import CredentialManager


class AgentConfigManager:
    """Manages agent configurations with persistent storage"""
    
    CONFIG_FILE = Path.home() / ".cloudcurio" / "agent_configs.json"
    
    def __init__(self):
        self.config_dir = Path.home() / ".cloudcurio"
        self.config_dir.mkdir(exist_ok=True)
        self.configs = self._load_configs()
    
    def _load_configs(self) -> Dict[str, Any]:
        """Load agent configurations from file"""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_configs(self):
        """Save agent configurations to file"""
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.configs, f, indent=2)
    
    def save_agent_config(self, agent_id: str, config: Dict[str, Any]):
        """Save configuration for a specific agent"""
        self.configs[agent_id] = config
        self._save_configs()
    
    def get_agent_config(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific agent"""
        return self.configs.get(agent_id)
    
    def list_agent_configs(self) -> List[str]:
        """List all saved agent configurations"""
        return list(self.configs.keys())
    
    def delete_agent_config(self, agent_id: str):
        """Delete configuration for a specific agent"""
        if agent_id in self.configs:
            del self.configs[agent_id]
            self._save_configs()
    
    def update_agent_provider(self, agent_id: str, provider: str, model: Optional[str] = None):
        """Update the provider for a specific agent"""
        config = self.get_agent_config(agent_id)
        if not config:
            raise ValueError(f"Agent configuration '{agent_id}' not found")
        
        config['provider'] = provider
        if model:
            config['model'] = model
        
        self.save_agent_config(agent_id, config)
    
    def get_agent_provider(self, agent_id: str) -> Optional[str]:
        """Get the provider for a specific agent"""
        config = self.get_agent_config(agent_id)
        return config.get('provider') if config else None


class GlobalConfigManager:
    """Manages global application configuration with secure credential storage"""
    
    GLOBAL_CONFIG_FILE = Path.home() / ".cloudcurio" / "global_config.json"
    
    def __init__(self):
        self.config_dir = Path.home() / ".cloudcurio"
        self.config_dir.mkdir(exist_ok=True)
        self.config = self._load_global_config()
    
    def _load_global_config(self) -> Dict[str, Any]:
        """Load global configuration from file"""
        if self.GLOBAL_CONFIG_FILE.exists():
            try:
                with open(self.GLOBAL_CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_global_config(self):
        """Save global configuration to file"""
        with open(self.GLOBAL_CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def set_default_provider(self, provider: str):
        """Set the default AI provider for the application"""
        self.config['default_provider'] = provider
        self._save_global_config()
    
    def get_default_provider(self) -> str:
        """Get the default AI provider for the application"""
        return self.config.get('default_provider', 'openrouter')
    
    def set_default_model(self, provider: str, model: str):
        """Set the default model for a specific provider"""
        if 'default_models' not in self.config:
            self.config['default_models'] = {}
        self.config['default_models'][provider] = model
        self._save_global_config()
    
    def get_default_model(self, provider: str) -> Optional[str]:
        """Get the default model for a specific provider"""
        if 'default_models' in self.config:
            return self.config['default_models'].get(provider)
        return None
    
    def add_api_key(self, provider: str, api_key: str):
        """Securely store an API key for a provider"""
        CredentialManager.store_credential(f"{provider.upper()}_API_KEY", api_key)
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Retrieve an API key for a provider"""
        return CredentialManager.get_credential(f"{provider.upper()}_API_KEY")
    
    def list_configured_providers(self) -> List[str]:
        """List providers that have API keys configured"""
        all_providers = [
            'openrouter', 'openai', 'gemini', 'ollama', 'localai', 
            'qwen', 'groq', 'grok', 'lmstudio', 'sambanova', 
            'deepinfra', 'modelsdev', 'litellm'
        ]
        
        configured = []
        for provider in all_providers:
            if CredentialManager.get_credential(f"{provider.upper()}_API_KEY"):
                configured.append(provider)
        
        return configured


# Global instances for easy access
agent_config_manager = AgentConfigManager()
global_config_manager = GlobalConfigManager()