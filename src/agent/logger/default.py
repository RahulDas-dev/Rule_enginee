import getpass
from typing import Any, Optional

from termcolor._types import Color

from .base import IOStream
from .utility import modify_logger_behaviour


class IODefault(IOStream):
    """A Default logger stream."""

    def __init__(self):
        super().__init__()
        self.logger = modify_logger_behaviour(__name__)

    def print(self, objects: Any, color: Optional[Color] = None) -> None:
        """Print data to the Deafault Logger.

        Args:
        ----
            objects (any): The data to print.
            color (str, optional): The terminal color to use.

        """
        if color is None:
            self.logger.info(objects)
        else:
            self.logger.info(objects, extra={"color": color})

    def input(self, prompt: str = "", *, password: bool = False) -> str:
        """Read a line from the input stream.

        Args:
        ----
            prompt (str, optional): The prompt to display. Defaults to "".
            password (bool, optional): Whether to read a password. Defaults to False.

        Returns:
        -------
            str: The line read from the input stream.

        """
        if password:
            return getpass.getpass(prompt if prompt != "" else "Password: ")
        return input(prompt)
