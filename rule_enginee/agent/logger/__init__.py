from .base import OutputStream, InputStream, IOStream
from .default import IODefault


IOStream.set(IODefault())


__all__ = ("OutputStream", "InputStream", "IOStream")
