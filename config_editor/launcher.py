#!/usr/bin/env python3
"""
CloudCurio Configuration Editor Launcher
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root.parent))

from config_editor.config_editor import ConfigEditorAPI


def main():
    print("Starting CloudCurio Configuration Editor...")
    
    # Initialize and run the API
    api = ConfigEditorAPI()
    
    print("CloudCurio Configuration Editor is running on http://localhost:8081")
    print("Features:")
    print("- Web interface for service and program management")
    print("- Action recording with Puppeteer")
    print("- AI-powered action categorization")
    print("- Step group management")
    
    api.run()


if __name__ == "__main__":
    main()