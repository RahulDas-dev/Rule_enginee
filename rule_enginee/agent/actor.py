import json
import logging
from typing import Any, Callable, Dict, List, Optional

from .client import ClientFactory

from .base import BaseMember
from .f_calling_utils import assert_valid_name, get_function_schema

logger = logging.getLogger(__name__)


class ActorLLM(BaseMember):
    _name: str
    _system_msg: str
    _examples: List[Dict[str, str]]
    _chat_history: List[Dict[str, str]]
    _llm_config: Optional[Dict]
    _function_map: Dict[str, Callable]

    def __init__(
        self,
        name: str,
        system_message: str = "You are a helpful AI Assistant.",
        llm_config: Optional[Dict] = None,
        examples: Optional[List[Dict]] = None,
        functions_list: Optional[List[Callable]] = None,
        enable_cache: bool = False,
        enable_logger: bool = True,
    ):
        self._name = name
        self._system_msg = system_message
        self._examples = [] if examples is None else examples
        if len(self._examples) % 2 != 0:
            raise ValueError("Examples is always multiple of 2")
        self._chat_history = [
            {"role": "system", "content": self._system_msg}
        ] + self._examples
        self._enable_cache = enable_cache
        self._enable_logger = enable_logger
        self._llm_config = llm_config.copy() if llm_config is not None else {}
        self._function_map = self._build_f_map(functions_list)
        self._client = ClientFactory.build(
            self._llm_config, self._enable_cache, self._enable_logger
        )

    def _build_f_map(
        self, function_map: Optional[list[Callable]] = None
    ) -> Dict[str, Callable]:
        if function_map is None:
            return {}
        f_map = {}
        tools = []
        for fitem in function_map.copy():
            if not callable(fitem):
                logger.warning(f"{fitem} is not a valid functions ...")
            fname = assert_valid_name(fitem.__name__)
            f_map[fname] = fitem
            f_signature = get_function_schema(fitem, name=fname)
            tools.append(f_signature)

        if tools:
            if self._llm_config is None:
                self._llm_config = {}
            self._llm_config["tools"] = tools
            self._llm_config["tool_choice"] = "auto"
        return f_map

    @property
    def has_chat_history(self) -> bool:
        return True if len(self._chat_history) > len(self._examples) + 1 else False

    @property
    def name(self) -> str:
        """The name of the agent."""
        return self._name

    @property
    def description(self) -> str:
        """The description of the agent. Used for the agent's introduction in
        a group chat setting."""
        return self._description

    @property
    def system_message(self) -> str:
        """The system message of this agent."""
        return self._system_msg

    def generate_reply(
        self, messages: Dict[str, str], **kwargs: Any
    ) -> Optional[Dict[str, str]]:
        messages_t = self._format_message(messages)
        self._chat_history.append(messages_t)
        if messages.get("tool_calls", None) is not None:
            messages_ = self._manage_f_calls(messages_t)
            if messages_ is not None:
                self._chat_history.append(messages_)
        response = self._client.response(self._chat_history)
        if response is not None:
            self._chat_history.append(response)
        return response

    def _manage_f_calls(self, messages) -> Dict[str, str]:
        tool_data = messages.get("tool_calls", [None])[0]
        if tool_data is None:
            return messages
        if tool_data.get("type", None) != "function":
            return messages

        function_name = tool_data.get("function", {}).get("name")
        function_args = json.loads(tool_data.get("function", {}).get("arguments"))
        func_item = self._function_map.get(function_name, None)
        if func_item is None:
            function_response = f"Function Not Found, for name {function_name}"
            logger.info(function_response)
            return {
                "tool_call_id": tool_data.get("id"),
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        try:
            function_response = func_item(**function_args)
        except Exception as e:
            logger.warn(
                f"Exception While the {function_name} Calling: {e} ", exc_info=True
            )
            function_response = repr(e)
        finally:
            return {
                "tool_call_id": tool_data.get("id"),
                "role": "tool",
                "name": function_name,
                "content": str(function_response),
            }

    def _format_message(self, messages: Dict[str, str]):
        return messages.copy()

    def resolve_task(self, task: str) -> Optional[str]:
        message = {"role": "user", "content": task}
        response = self.generate_reply(message)
        if response is None:
            logger.error("Response is None")
            return None
        while response.get("tool_calls", None) is not None:
            messages_ = self._manage_f_calls(response)
            if messages_ is None:
                logger.error("Response is None")
                return None
            response = self.generate_reply(messages_)
            if response is None:
                logger.error("Response is None")
                return None
        return self._extract_result_from_chat()

    def _extract_result_from_chat(self) -> Optional[str]:
        return self._chat_history[-1].get("content", None)

    @property
    def chat_history(self) -> List[Dict[str, str]]:
        """Returns the Chat history"""
        return self._chat_history.copy()

    def reset_chat_history(self):
        self._chat_history = [
            {"role": "system", "content": self._system_msg}
        ] + self._examples.copy()

    def update_system_msg(self, system_message: str):
        self._system_msg = system_message
        if len(self._examples) % 2 != 0:
            raise ValueError("Examples is always multiple of 2")
        self._chat_history = [
            {"role": "system", "content": self._system_msg}
        ] + self._examples
