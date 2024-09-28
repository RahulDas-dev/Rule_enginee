from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Integer, String

from src.db.pydantic_col_type import PydanticColumn
from src.estimator.schemas import ChatHistory, QueryList

from .base import Base


class RulesInfo(Base):
    __tablename__ = "rules_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    version: Mapped[str] = mapped_column(String(), nullable=False)
    rules_input: Mapped[str] = mapped_column(String(), nullable=False)
    agent_reponse: Mapped[str] = mapped_column(String(), nullable=False)
    querys: Mapped[QueryList] = mapped_column(PydanticColumn(QueryList), nullable=False, default=QueryList())
    agent_chat_history: Mapped[ChatHistory] = mapped_column(
        PydanticColumn(ChatHistory),
        nullable=False,
        default=ChatHistory(),
    )
    status: Mapped[str] = mapped_column(String(), nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=False, server_default=func.now())

    __table_args__ = (UniqueConstraint("version", name="rules_info_version_uc"),)
