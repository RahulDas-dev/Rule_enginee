from .base import InputStream, IOStream, OutputStream
from .default import IODefault

IOStream.set(IODefault())


__all__ = ("OutputStream", "InputStream", "IOStream")
