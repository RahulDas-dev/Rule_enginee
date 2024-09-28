import sqlalchemy
from sqlalchemy.orm import DeclarativeBase

meta = sqlalchemy.MetaData(schema=None)


class Base(DeclarativeBase):
    """Base for all DB models."""

    metadata = meta
