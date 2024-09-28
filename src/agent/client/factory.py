from typing import Any, Dict, Literal

from .llmclient import LlmClient

ClientType = Literal["finaclegpt432k", "Gemeni", "claude-3-opus", "codechat-bison", "Gemini"]


DEFAULT_CONFIG = {
    "temperature": 0.1,
    "timeout": 600,
    "num_retries": 3,
}

GPT4O_DEFAULT_CONFIG = {**DEFAULT_CONFIG, "max_tokens": 4096}

ANTHROPIC_DEFAULT_CONFIG = {**DEFAULT_CONFIG, "max_tokens": 4096}

GEMINI_DEFAULT_CONFIG = {**DEFAULT_CONFIG, "max_tokens": 4096}


class ClientFactory:
    @staticmethod
    def build(config: Dict[str, Any], enenable_cache: bool = False, enable_logger: bool = True) -> LlmClient:
        config_ = config.copy()
        client_type: ClientType = config_.get("model", None)
        if client_type == "finaclegpt432k":
            config_ = {**DEFAULT_CONFIG, **config}
            config_["model"] = "azure/finaclegpt432k"
        elif client_type == "finaclegpt4o":
            config_["model"] = "azure/finaclegpt4o"
            config_ = {**GPT4O_DEFAULT_CONFIG, **config}
        elif client_type == "claude-3-opus":
            config_ = {**ANTHROPIC_DEFAULT_CONFIG, **config}
            config_["model"] = "vertex_ai/claude-3-opus@20240229"
        elif client_type == "Gemini":
            config_ = {**GEMINI_DEFAULT_CONFIG, **config}
            config_["model"] = "vertex_ai/gemini-pro"
        else:
            raise TypeError("Client is Not Suppoeted yet")
        return LlmClient(config_, enenable_cache, enable_logger)
