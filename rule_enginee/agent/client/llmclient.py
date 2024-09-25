import logging
from typing import Any, Dict, List, Optional

from litellm import completion, stream_chunk_builder
from litellm.types.utils import ModelResponse
from termcolor._types import Color

from ..logger import IOStream

from .base import BaseClient

logger = logging.getLogger(__name__)


class LlmClient(BaseClient):
    _config: Dict
    _enable_cache: bool
    _enable_logger: bool

    def __init__(self, config, enable_cache: bool = False, enable_logger: bool = True):
        self._model_name = config.pop("model")
        self._configs = config.copy()
        self._enable_cache = enable_cache
        self._enable_logger = enable_logger
        self._iostream = IOStream.get()

    @property
    def model_name(self) -> str:
        return self._model_name

    def log(self, objects: Any, color: Optional[Color] = None) -> None:
        if not self._enable_logger:
            return
        color_ = "green" if color is None else color
        self._iostream.print(objects, color=color_)

    def response(self, messages: List[Dict[str, str]], stream: bool = True) -> Optional[Dict]:
        reply_msg = None
        if stream:
            reply_msg = self._response_in_stream(messages)
        else:
            reply_msg = self._response_in_nonstream(messages)
        return reply_msg

    def _response_in_stream(self, messages: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
        response, reply_msg = None, None
        try:
            response = completion(
                model=self.model_name,
                messages=messages,
                stream=True,
                caching=self._enable_cache,
                **self._configs,
            )
        except Exception as err:
            logger.info(f"Error While LLM Call , Error {err}")
            reply_msg = None
        else:
            chunks = []
            for chunk in response:
                chunks.append(chunk)
                chunk_var = chunk["choices"][0]["delta"]  # type: ignore
                if chunk_var.get("content", None) is not None:
                    self.log(chunk_var["content"])
                else:
                    pass
            message_final = stream_chunk_builder(chunks, messages=messages)
            reply_msg = message_final.choices[0]["message"].model_dump()
            if reply_msg.get("tool_calls", None) is not None:
                self.log(reply_msg["tool_calls"])
            self.log("\n")
        finally:
            return reply_msg

    def _response_in_nonstream(self, messages: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
        response, reply_msg = None, None
        try:
            response = completion(
                model=self.model_name,
                messages=messages,
                caching=self._enable_cache,
                stream=False,
                **self._configs,
            )
        except Exception as err:
            logger.error(f"Error While LLM Call , Error {err}")
            reply_msg = None
        else:
            reply_msg = response.choices[0]["message"].model_dump() if isinstance(response, ModelResponse) else None
            if reply_msg is not None:
                if reply_msg.get("content", None) is not None:
                    self.log(reply_msg.get("content"))
                else:
                    self.log(reply_msg.get("tool_calls"))
            else:
                self.log("No response", color="blue")
            self.log("\n")
        finally:
            return reply_msg
