"""
AI Model Adapters for multi-provider support.
Supports: Azure OpenAI, Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google)
"""
import os
import logging
from typing import Optional

logger = logging.getLogger("sentinel-middleware")


class BaseAdapter:
    """Base class for AI model adapters."""

    _CHAT_PARAMS = frozenset(("temperature", "max_tokens"))

    def _chat_kwargs(self, kwargs: dict) -> dict:
        """Filter kwargs to only the parameters supported by chat completion APIs."""
        return {k: v for k, v in kwargs.items() if k in self._CHAT_PARAMS}

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement generate()")


class AzureOpenAIAdapter(BaseAdapter):
    """Azure OpenAI adapter."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        if not all([self.endpoint, self.deployment, self.api_key]):
            logger.warning("Azure OpenAI config incomplete - using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        logger.info(f"🧬 Azure OpenAI ritual invoked by {user_id}: {prompt[:50]}...")
        if not all([self.endpoint, self.api_key]):
            return f"[Azure OpenAI Mock] {prompt}"
        try:
            from openai import AzureOpenAI
            client = AzureOpenAI(
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            )
            response = client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                **self._chat_kwargs(kwargs),
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.error(f"Azure OpenAI error: {exc}")
            return f"[Azure OpenAI Mock] {prompt}"


class ClaudeAdapter(BaseAdapter):
    """Anthropic Claude adapter."""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        if not self.api_key:
            logger.warning("ANTHROPIC_API_KEY not set - using mock responses")
    
    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        logger.info(f"🧬 Claude ritual invoked by {user_id}: {prompt[:50]}...")
        if not self.api_key:
            return f"[Claude Mock] {prompt}"
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            max_tokens = kwargs.get("max_tokens", 1024)
            message = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text if message.content else ""
        except Exception as exc:
            logger.error(f"Claude error: {exc}")
            return f"[Claude Mock] {prompt}"


class ChatGPTAdapter(BaseAdapter):
    """OpenAI ChatGPT adapter."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set - using mock responses")
    
    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        logger.info(f"🧬 ChatGPT ritual invoked by {user_id}: {prompt[:50]}...")
        if not self.api_key:
            return f"[ChatGPT Mock] {prompt}"
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **self._chat_kwargs(kwargs),
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.error(f"ChatGPT error: {exc}")
            return f"[ChatGPT Mock] {prompt}"


class GeminiAdapter(BaseAdapter):
    """Google Gemini adapter (via OpenAI-compatible endpoint)."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not set - using mock responses")
    
    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        logger.info(f"🧬 Gemini ritual invoked by {user_id}: {prompt[:50]}...")
        if not self.api_key:
            return f"[Gemini Mock] {prompt}"
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            )
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **self._chat_kwargs(kwargs),
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.error(f"Gemini error: {exc}")
            return f"[Gemini Mock] {prompt}"


def get_model_adapter(provider: Optional[str] = None) -> BaseAdapter:
    """Factory function to get the appropriate model adapter, prioritizing Azure."""
    # 1. Prioritize Azure OpenAI if configured
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if azure_endpoint and azure_deployment:
        logger.info("Using AI provider: Azure OpenAI")
        return AzureOpenAIAdapter()

    # 2. Fallback to QNF_MODEL_PROVIDER if Azure is not configured
    if provider is None:
        provider = os.getenv("QNF_MODEL_PROVIDER", "chatgpt").lower()
    
    adapters = {
        "claude": ClaudeAdapter,
        "chatgpt": ChatGPTAdapter,
        "gemini": GeminiAdapter,
    }
    
    adapter_class = adapters.get(provider, ChatGPTAdapter)
    logger.info(f"Using AI provider: {provider}")
    return adapter_class()
