#!/usr/bin/env python3
"""
CloudCurio Configuration CLI

A command-line tool to manage AI provider credentials and agent configurations.
"""

import argparse
import sys
import getpass
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai_tools.ai_provider import (
    CredentialManager, 
    ai_manager as provider_manager,
    OpenRouterProvider,
    OpenAIProvider,
    GoogleGeminiProvider,
    OllamaProvider,
    LocalAIProvider,
    QwenProvider,
    GroqProvider,
    GrokProvider,
    LMStudioProvider,
    SambaNovaProvider,
    DeepInfraProvider,
    ModelsDevProvider,
    LiteLLMProvider
)
from ai_tools.config_manager import (
    agent_config_manager,
    global_config_manager
)


def setup_command(args):
    """Setup command to initialize CloudCurio configuration"""
    print("Setting up CloudCurio configuration...")
    
    # Create config directory
    config_dir = Path.home() / ".cloudcurio"
    config_dir.mkdir(exist_ok=True)
    print(f"Configuration directory created at: {config_dir}")
    
    # Check if GPG is available
    if not CredentialManager.has_gpg():
        print("WARNING: GPG not found. Credentials will be stored in environment variables only.")
        print("For enhanced security, install GPG on your system.")
    else:
        print("GPG is available for secure credential storage.")
    
    print("Setup complete!")


def add_credential_command(args):
    """Command to add a credential"""
    print(f"Adding credential for {args.provider}...")
    
    # Get the API key securely
    api_key = getpass.getpass(f"Enter API key for {args.provider}: ")
    
    # Store the credential securely
    global_config_manager.add_api_key(args.provider, api_key)
    print(f"API key for {args.provider} stored successfully!")


def list_providers_command(args):
    """Command to list available providers"""
    print("Available AI Providers:")
    providers = [
        "openrouter", "openai", "gemini", "ollama", "localai", 
        "qwen", "groq", "grok", "lmstudio", "sambanova", 
        "deepinfra", "modelsdev", "litellm"
    ]
    
    for provider in providers:
        is_available = global_config_manager.get_api_key(provider) is not None
        status = "✓ Configured" if is_available else "✗ Not configured"
        print(f"  - {provider}: {status}")


def test_provider_command(args):
    """Command to test a provider"""
    print(f"Testing provider: {args.provider}")
    
    try:
        if provider_manager.is_provider_available(args.provider):
            print(f"✓ Provider {args.provider} is available!")
            
            # Get available models
            models = provider_manager.get_provider_models(args.provider)
            if models:
                print(f"Available models: {models[:5]}{'...' if len(models) > 5 else ''}")
        else:
            print(f"✗ Provider {args.provider} is not available (missing API key or service unreachable)")
    except Exception as e:
        print(f"✗ Error testing provider {args.provider}: {str(e)}")


def set_default_provider_command(args):
    """Command to set the default provider"""
    print(f"Setting default provider to: {args.provider}")
    
    # Check if provider has credentials
    if global_config_manager.get_api_key(args.provider):
        global_config_manager.set_default_provider(args.provider)
        print(f"✓ Default provider set to {args.provider}")
    else:
        print(f"✗ Provider {args.provider} does not have credentials configured")
        print(f"  Use 'cloudcurio add-credential {args.provider}' to add credentials")


def list_agents_command(args):
    """Command to list agent configurations"""
    print("Configured Agents:")
    agent_configs = agent_config_manager.list_agent_configs()
    
    if not agent_configs:
        print("  No agents configured")
    else:
        for agent_id in agent_configs:
            config = agent_config_manager.get_agent_config(agent_id)
            provider = config.get('provider', 'Not set')
            model = config.get('model', 'Not set')
            print(f"  - {agent_id}: {provider}/{model}")


def configure_agent_command(args):
    """Command to configure an agent"""
    print(f"Configuring agent: {args.agent_id}")
    
    # Get current config or create new one
    config = agent_config_manager.get_agent_config(args.agent_id) or {}
    
    # Update provider if specified
    if args.provider:
        config['provider'] = args.provider
        print(f"  Provider set to: {args.provider}")
    
    # Update model if specified
    if args.model:
        config['model'] = args.model
        print(f"  Model set to: {args.model}")
    
    # Save the configuration
    agent_config_manager.save_agent_config(args.agent_id, config)
    print(f"✓ Agent {args.agent_id} configured!")


def main():
    parser = argparse.ArgumentParser(description="CloudCurio Configuration CLI")
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup CloudCurio configuration")
    setup_parser.set_defaults(func=setup_command)
    
    # Add credential command
    credential_parser = subparsers.add_parser("add-credential", help="Add a credential for a provider")
    credential_parser.add_argument("provider", help="Provider name (e.g., openai, gemini, etc.)")
    credential_parser.set_defaults(func=add_credential_command)
    
    # List providers command
    list_parser = subparsers.add_parser("list-providers", help="List available providers")
    list_parser.set_defaults(func=list_providers_command)
    
    # Test provider command
    test_parser = subparsers.add_parser("test-provider", help="Test if a provider is available")
    test_parser.add_argument("provider", help="Provider name to test")
    test_parser.set_defaults(func=test_provider_command)
    
    # Set default provider command
    default_parser = subparsers.add_parser("set-default", help="Set the default provider")
    default_parser.add_argument("provider", help="Provider name to set as default")
    default_parser.set_defaults(func=set_default_provider_command)
    
    # List agents command
    list_agents_parser = subparsers.add_parser("list-agents", help="List configured agents")
    list_agents_parser.set_defaults(func=list_agents_command)
    
    # Configure agent command
    configure_parser = subparsers.add_parser("configure-agent", help="Configure an agent")
    configure_parser.add_argument("agent_id", help="ID of the agent to configure")
    configure_parser.add_argument("--provider", help="Provider for the agent")
    configure_parser.add_argument("--model", help="Model for the agent")
    configure_parser.set_defaults(func=configure_agent_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the appropriate function
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()