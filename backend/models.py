"""
AI Model Adapters for multi-provider support.
Supports: Azure OpenAI, Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google)

Each adapter uses the respective SDK/API when the API key is configured,
and falls back to a descriptive mock response otherwise.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger("sentinel-middleware")


class BaseAdapter:
    """Base class for AI model adapters."""

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement generate()")


class AzureOpenAIAdapter(BaseAdapter):
    """Azure OpenAI adapter using the openai SDK with Azure configuration."""

    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self._client = None
        if self.endpoint and self.deployment and self.api_key:
            try:
                from openai import AzureOpenAI
                self._client = AzureOpenAI(
                    azure_endpoint=self.endpoint,
                    api_key=self.api_key,
                    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
                )
            except Exception as e:
                logger.warning("Failed to init Azure OpenAI client: %s", e)
        else:
            logger.warning("Azure OpenAI config incomplete — using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        if not self._client:
            return f"[Azure OpenAI mock] {prompt}"
        try:
            resp = self._client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 1024),
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            logger.error("Azure OpenAI generation failed: %s", e)
            return f"[Azure OpenAI error] {e}"


class ClaudeAdapter(BaseAdapter):
    """Anthropic Claude adapter using the anthropic SDK."""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self._client = None
        if self.api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                logger.warning("anthropic package not installed — using mock responses")
            except Exception as e:
                logger.warning("Failed to init Anthropic client: %s", e)
        else:
            logger.warning("ANTHROPIC_API_KEY not set — using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        if not self._client:
            return f"[Claude mock] {prompt}"
        try:
            resp = self._client.messages.create(
                model=kwargs.get("model", "claude-sonnet-4-20250514"),
                max_tokens=kwargs.get("max_tokens", 1024),
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text if resp.content else ""
        except Exception as e:
            logger.error("Claude generation failed: %s", e)
            return f"[Claude error] {e}"


class ChatGPTAdapter(BaseAdapter):
    """OpenAI ChatGPT adapter using the openai SDK."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning("Failed to init OpenAI client: %s", e)
        else:
            logger.warning("OPENAI_API_KEY not set — using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        if not self._client:
            return f"[ChatGPT mock] {prompt}"
        try:
            resp = self._client.chat.completions.create(
                model=kwargs.get("model", "gpt-4"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 1024),
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            logger.error("ChatGPT generation failed: %s", e)
            return f"[ChatGPT error] {e}"


class GeminiAdapter(BaseAdapter):
    """Google Gemini adapter using the google-generativeai SDK."""

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self._model = None
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel("gemini-pro")
            except ImportError:
                logger.warning("google-generativeai package not installed — using mock responses")
            except Exception as e:
                logger.warning("Failed to init Gemini client: %s", e)
        else:
            logger.warning("GOOGLE_API_KEY not set — using mock responses")

    def generate(self, prompt: str, user_id: str, **kwargs) -> str:
        if not self._model:
            return f"[Gemini mock] {prompt}"
        try:
            resp = self._model.generate_content(prompt)
            return resp.text or ""
        except Exception as e:
            logger.error("Gemini generation failed: %s", e)
            return f"[Gemini error] {e}"


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
    logger.info("Using AI provider: %s", provider)
    return adapter_class()
