from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from termcolor._types import Color


@runtime_checkable
class BaseClient(Protocol):
    @property
    def model_name(self) -> str:
        """Returns Model name"""
        ...

    def response(
        self, messages: List[Dict[str, str]], stream: bool = True
    ) -> Optional[Dict[str, str]]:
        """
        Generates Response for Given Chat.

        Returns:
            chat_res (Dict):
        """
        ...

    def log(
        self,
        objects: Any,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
        color: Optional[Color] = None,
    ):
        """
        Prints Response for Given Chat.
        """
        ...
