from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import yaml
import os

class Plugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'unnamed-plugin')
        self.version = config.get('version', '1.0.0')
        self.description = config.get('description', '')
        self.type = config.get('type', 'generic')
        self.enabled = config.get('enabled', True)
        self.dependencies = config.get('dependencies', [])
        
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin. Return True if successful."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the plugin's main functionality"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources"""
        pass
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def validate_config(self) -> bool:
        """Validate the plugin configuration"""
        # Basic validation - check if required fields are present
        required_fields = ['name', 'version', 'description']
        for field in required_fields:
            if field not in self.config:
                return False
        return True

class PluginManager:
    """Manages the lifecycle of plugins"""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_configs: Dict[str, Dict[str, Any]] = {}
        
    def discover_plugins(self) -> List[str]:
        """Discover available plugins"""
        plugin_names = []
        if os.path.exists(self.plugins_dir):
            for item in os.listdir(self.plugins_dir):
                plugin_path = os.path.join(self.plugins_dir, item)
                if os.path.isdir(plugin_path):
                    config_file = os.path.join(plugin_path, 'plugin.yaml')
                    if os.path.exists(config_file):
                        plugin_names.append(item)
        return plugin_names
    
    def load_plugin_config(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Load plugin configuration"""
        config_file = os.path.join(self.plugins_dir, plugin_name, 'plugin.yaml')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                self.plugin_configs[plugin_name] = config
                return config
        return None
    
    def load_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """Load a plugin by name"""
        # Load configuration
        config = self.load_plugin_config(plugin_name)
        if not config:
            return None
            
        # Create plugin instance
        try:
            # Import plugin module
            plugin_module = __import__(f"plugins.{plugin_name}.plugin", fromlist=['PluginImplementation'])
            plugin_class = getattr(plugin_module, 'PluginImplementation')
            
            # Create instance
            plugin = plugin_class(config)
            
            # Validate configuration
            if not plugin.validate_config():
                print(f"Invalid configuration for plugin {plugin_name}")
                return None
                
            # Initialize plugin
            if plugin.initialize():
                self.plugins[plugin_name] = plugin
                return plugin
            else:
                print(f"Failed to initialize plugin {plugin_name}")
                return None
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            return None
    
    def load_all_plugins(self) -> None:
        """Load all discovered plugins"""
        plugin_names = self.discover_plugins()
        for plugin_name in plugin_names:
            self.load_plugin(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """Get a loaded plugin by name"""
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """List all loaded plugins"""
        return list(self.plugins.keys())
    
    def execute_plugin(self, plugin_name: str, **kwargs) -> Any:
        """Execute a plugin by name"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            return plugin.execute(**kwargs)
        else:
            raise ValueError(f"Plugin {plugin_name} not found or not loaded")
    
    def unload_plugin(self, plugin_name: str) -> None:
        """Unload a plugin"""
        plugin = self.plugins.get(plugin_name)
        if plugin:
            plugin.cleanup()
            del self.plugins[plugin_name]
    
    def unload_all_plugins(self) -> None:
        """Unload all plugins"""
        for plugin in list(self.plugins.values()):
            plugin.cleanup()
        self.plugins.clear()