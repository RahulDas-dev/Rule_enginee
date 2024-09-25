from sqlalchemy.orm import DeclarativeBase

from ..metadata import meta


class Base(DeclarativeBase):
    """Base for all DB models."""

    metadata = meta
