import logging
from typing import Any, Optional, Protocol, runtime_checkable

from termcolor._types import Color

logger = logging.getLogger(__name__)


@runtime_checkable
class OutputStream(Protocol):
    def print(
        self,
        *objects: Any,
        color: Optional[Color] = None,
    ) -> None:
        """Print data to the output stream.

        Args:
        ----
            objects (any): The data to print.
            sep (str, optional): The separator between objects. Defaults to " ".
            end (str, optional): The end of the output. Defaults to "\n".
            flush (bool, optional): Whether to flush the output. Defaults to False.

        """
        ...  # pragma: no cover


@runtime_checkable
class InputStream(Protocol):
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
        ...  # pragma: no cover


@runtime_checkable
class IOStream(InputStream, OutputStream, Protocol):
    """A protocol for input/output streams."""

    _io_stream: Optional["IOStream"]

    @staticmethod
    def set(stream: "IOStream") -> None:
        """Set the default input/output stream.

        Args:
        ----
            stream (IOStream): The input/output stream to set as the default.

        """
        IOStream._io_stream = stream

    @staticmethod
    def get() -> "IOStream":
        """Get the default input/output stream.

        Returns
        -------
            IOStream: The default input/output stream.

        """
        iostream = IOStream._io_stream
        return iostream
