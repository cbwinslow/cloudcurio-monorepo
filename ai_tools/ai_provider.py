"""
Enhanced AI Provider Manager with secure credential storage

This module provides integration with multiple AI providers with secure
credential management using GPG encryption for local storage.
"""

import os
import json
import subprocess
import tempfile
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from pathlib import Path


class BaseAIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the AI model"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the AI provider is available and properly configured"""
        pass
    
    @abstractmethod
    def get_model_list(self) -> List[str]:
        """Get a list of available models for this provider"""
        pass


class OpenRouterProvider(BaseAIProvider):
    """OpenRouter API provider with multiple model support"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("OpenRouter API key not configured")
        
        import requests
        
        model = kwargs.get("model", self.default_model)
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        if not self.is_available():
            return []
        
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        try:
            response = requests.get(f"{self.base_url}/models", headers=headers)
            response.raise_for_status()
            models = response.json()["data"]
            return [model["id"] for model in models]
        except:
            # Fallback to a common list of models
            return [
                "mistralai/mistral-7b-instruct", 
                "google/gemini-pro", 
                "openai/gpt-3.5-turbo",
                "openai/gpt-4"
            ]


class OpenAIProvider(BaseAIProvider):
    """OpenAI API provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")
        
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def get_model_list(self) -> List[str]:
        if not self.is_available():
            return []
        
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        try:
            models = client.models.list()
            return [model.id for model in models.data]
        except:
            # Fallback to common OpenAI models
            return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]


class GoogleGeminiProvider(BaseAIProvider):
    """Google Gemini API provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Gemini API key not configured")
        
        import google.generativeai as genai
        
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        
        # Convert kwargs to generation config
        generation_config = {}
        if "temperature" in kwargs:
            generation_config["temperature"] = kwargs["temperature"]
        if "max_output_tokens" in kwargs:
            generation_config["max_output_tokens"] = kwargs["max_output_tokens"]
        if "top_p" in kwargs:
            generation_config["top_p"] = kwargs["top_p"]
        if "top_k" in kwargs:
            generation_config["top_k"] = kwargs["top_k"]
        
        safety_settings = [
            {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        ]
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        return response.text
    
    def get_model_list(self) -> List[str]:
        if not self.is_available():
            return []
        
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        
        try:
            models = genai.list_models()
            return [model.name.replace("models/", "") for model in models]
        except:
            return ["gemini-pro", "gemini-1.5-pro-latest", "gemini-1.5-flash"]


class OllamaProvider(BaseAIProvider):
    """Local Ollama provider"""
    
    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "llama3")
        self.base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Ollama service not available")
        
        import requests
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        data.update(kwargs)
        
        response = requests.post(f"{self.base_url}/api/generate", json=data)
        response.raise_for_status()
        
        return response.json()["response"]
    
    def get_model_list(self) -> List[str]:
        if not self.is_available():
            return []
        
        import requests
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json()["models"]
            return [model["name"] for model in models]
        except:
            return ["llama3", "mistral", "phi3"]


class LocalAIProvider(BaseAIProvider):
    """LocalAI provider (compatible with OpenAI API)"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("LOCALAI_API_KEY") or "dummy"
        self.base_url = os.getenv("LOCALAI_BASE_URL", "http://localhost:8080/v1")
        self.model = os.getenv("LOCALAI_MODEL", "default-model")
    
    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url.replace('/v1', '')}/models")
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("LocalAI service not available")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        if not self.is_available():
            return []
        
        import requests
        
        try:
            response = requests.get(f"{self.base_url.replace('/v1', '')}/models")
            response.raise_for_status()
            models = response.json()["data"]
            return [model["id"] for model in models]
        except:
            return ["default-model"]


class QwenProvider(BaseAIProvider):
    """Alibaba Qwen provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("QWEN_API_KEY")
        self.model = os.getenv("QWEN_MODEL", "qwen-max")
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Qwen API key not configured")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        # Qwen doesn't have a public API to list models, so return common ones
        return ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-1201", "qwen-max-longcontext"]


class GroqProvider(BaseAIProvider):
    """Groq API provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Groq API key not configured")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        return [
            "llama3-70b-8192",
            "llama3-8b-8192", 
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]


class GrokProvider(BaseAIProvider):
    """Grok from xAI provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("GROK_API_KEY")
        self.model = os.getenv("GROK_MODEL", "grok-beta")
        self.base_url = os.getenv("GROK_BASE_URL", "https://api.grok.xai.com/v1")
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Grok API key not configured")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        return ["grok-beta"]  # Currently Grok only has one model


class LMStudioProvider(BaseAIProvider):
    """LM Studio provider (OpenAI-compatible local server)"""
    
    def __init__(self):
        self.api_key = os.getenv("LMSTUDIO_API_KEY") or "dummy"
        self.base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
        self.model = os.getenv("LMSTUDIO_MODEL", "default-model")
    
    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/models")
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("LM Studio service not available")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        if not self.is_available():
            return []
        
        import requests
        
        try:
            response = requests.get(f"{self.base_url}/models")
            response.raise_for_status()
            models = response.json()["data"]
            return [model["id"] for model in models]
        except:
            return ["default-model"]


class SambaNovaProvider(BaseAIProvider):
    """SambaNova provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("SAMBANOVA_API_KEY")
        self.model = os.getenv("SAMBANOVA_MODEL", "Meta-Llama-3.1-8B")
        self.base_url = "https://api.sambanova.ai/v1"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("SambaNova API key not configured")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        # SambaNova doesn't have a public API to list models, return common ones
        return [
            "Meta-Llama-3.1-8B",
            "Meta-Llama-3.1-70B",
            "Meta-Llama-3.1-405B"
        ]


class DeepInfraProvider(BaseAIProvider):
    """DeepInfra provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("DEEPINFRA_API_KEY")
        self.model = os.getenv("DEEPINFRA_MODEL", "meta-llama/Meta-Llama-3.1-70B-Instruct")
        self.base_url = "https://api.deepinfra.com/v1/openai"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("DeepInfra API key not configured")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        # DeepInfra hosts many models, return a representative sample
        return [
            "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "mistralai/Mistral-Nemo-Instruct-2407",
            "microsoft/WizardLM-2-8x22B",
            "google/gemma-2-27b-it"
        ]


class ModelsDevProvider(BaseAIProvider):
    """Models.dev provider"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("MODELSD_EV_API_KEY")
        self.model = os.getenv("MODELSD_EV_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
        self.base_url = "https://models.dev/v1"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Models.dev API key not configured")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        # Models.dev provides many open-source models
        return [
            "mistralai/Mistral-7B-Instruct-v0.1",
            "google/gemma-7b-it",
            "meta-llama/Llama-2-7b-chat-hf",
            "codellama/CodeLlama-7b-Instruct-hf"
        ]


class LiteLLMProvider(BaseAIProvider):
    """LiteLLM provider (proxy for multiple LLM providers)"""
    
    def __init__(self):
        self.api_key = CredentialManager.get_credential("LITELLM_API_KEY")
        self.model = os.getenv("LITELLM_MODEL", "openai/gpt-3.5-turbo")
        self.base_url = os.getenv("LITELLM_BASE_URL", "http://localhost:4000/v1")
    
    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/models")
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("LiteLLM service not available")
        
        import requests
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        data.update({k: v for k, v in kwargs.items() if k != "model"})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_model_list(self) -> List[str]:
        if not self.is_available():
            return []
        
        import requests
        
        try:
            response = requests.get(f"{self.base_url}/models")
            response.raise_for_status()
            models = response.json()["data"]
            return [model["id"] for model in models]
        except:
            return ["openai/gpt-3.5-turbo"]


class CredentialManager:
    """Secure credential manager using GPG encryption for storage"""
    
    CREDENTIALS_FILE = Path.home() / ".cloudcurio" / "credentials.json.gpg"
    
    @classmethod
    def _ensure_config_dir(cls):
        """Ensure the config directory exists"""
        cls.CREDENTIALS_FILE.parent.mkdir(exist_ok=True)
    
    @classmethod
    def _encrypt_data(cls, data: str) -> bytes:
        """Encrypt data using GPG"""
        cls._ensure_config_dir()
        
        # Write data to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(data)
            temp_file_path = temp_file.name
        
        try:
            # Encrypt the temporary file using GPG
            result = subprocess.run([
                'gpg', '--encrypt', '--symmetric', '--batch', '--passphrase', 
                os.getenv('CLOUDCURIO_PASSPHRASE', 'default_passphrase'),
                '--output', str(cls.CREDENTIALS_FILE), temp_file_path
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"GPG encryption failed: {result.stderr}")
                
            return cls.CREDENTIALS_FILE.read_bytes()
        finally:
            # Remove the temporary file
            os.unlink(temp_file_path)
    
    @classmethod
    def _decrypt_data(cls) -> str:
        """Decrypt data using GPG"""
        if not cls.CREDENTIALS_FILE.exists():
            return '{}'
        
        # Write encrypted data to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(cls.CREDENTIALS_FILE.read_bytes())
            temp_encrypted_path = temp_file.name
        
        # Create another temporary file for output
        with tempfile.NamedTemporaryFile(delete=False) as temp_output:
            temp_output_path = temp_output.name
        
        try:
            # Decrypt the temporary file using GPG
            result = subprocess.run([
                'gpg', '--decrypt', '--batch', '--passphrase', 
                os.getenv('CLOUDCURIO_PASSPHRASE', 'default_passphrase'),
                '--output', temp_output_path, temp_encrypted_path
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"GPG decryption failed: {result.stderr}")
            
            with open(temp_output_path, 'r') as f:
                return f.read()
        finally:
            # Remove temporary files
            os.unlink(temp_encrypted_path)
            os.unlink(temp_output_path)
    
    @classmethod
    def store_credential(cls, key: str, value: str):
        """Store an encrypted credential"""
        # Load existing credentials
        try:
            creds_str = cls._decrypt_data()
            credentials = json.loads(creds_str) if creds_str.strip() else {}
        except:
            credentials = {}
        
        # Add or update the credential
        credentials[key] = value
        
        # Encrypt and save the credentials
        creds_json = json.dumps(credentials)
        cls._encrypt_data(creds_json)
    
    @classmethod
    def get_credential(cls, key: str) -> Optional[str]:
        """Retrieve a credential"""
        try:
            creds_str = cls._decrypt_data()
            credentials = json.loads(creds_str) if creds_str.strip() else {}
            return credentials.get(key) or os.getenv(key)
        except:
            # If decryption fails, fall back to environment variables
            return os.getenv(key)
    
    @classmethod
    def has_gpg(cls) -> bool:
        """Check if GPG is available"""
        try:
            result = subprocess.run(['gpg', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False


class AIProviderManager:
    """Manager for different AI providers with secure credential storage"""
    
    def __init__(self):
        # Initialize all providers
        self.providers: Dict[str, BaseAIProvider] = {
            "openrouter": OpenRouterProvider(),
            "openai": OpenAIProvider(),
            "gemini": GoogleGeminiProvider(),
            "ollama": OllamaProvider(),
            "localai": LocalAIProvider(),
            "qwen": QwenProvider(),
            "groq": GroqProvider(),
            "grok": GrokProvider(),
            "lmstudio": LMStudioProvider(),
            "sambanova": SambaNovaProvider(),
            "deepinfra": DeepInfraProvider(),
            "modelsdev": ModelsDevProvider(),
            "litellm": LiteLLMProvider(),
        }
        
        # Set default provider
        self.default_provider = os.getenv("DEFAULT_AI_PROVIDER", "openrouter")
    
    def get_provider(self, provider_name: Optional[str] = None) -> BaseAIProvider:
        """Get a specific provider or the default one"""
        provider_name = provider_name or self.default_provider
        
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}. Available: {list(self.providers.keys())}")
        
        provider = self.providers[provider_name]
        if not provider.is_available():
            raise ValueError(f"Provider {provider_name} is not available (missing API key or service unavailable)")
        
        return provider
    
    def generate_with_provider(self, prompt: str, provider_name: Optional[str] = None, **kwargs) -> str:
        """Generate using a specific provider"""
        provider = self.get_provider(provider_name)
        return provider.generate(prompt, **kwargs)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using the default provider"""
        return self.generate_with_provider(prompt, **kwargs)
    
    def list_providers(self) -> List[str]:
        """List all available providers"""
        return list(self.providers.keys())
    
    def get_provider_models(self, provider_name: str) -> List[str]:
        """Get available models for a specific provider"""
        try:
            provider = self.get_provider(provider_name)
            return provider.get_model_list()
        except:
            return []
    
    def is_provider_available(self, provider_name: str) -> bool:
        """Check if a specific provider is available"""
        try:
            provider = self.get_provider(provider_name)
            return provider.is_available()
        except:
            return False


# Global instance for easy access
ai_manager = AIProviderManager()