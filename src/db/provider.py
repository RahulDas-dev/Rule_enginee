import logging
from typing import Generator

from fastapi import Request
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def get_db_session(request: Request) -> Generator[Session, None, None]:
    """Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: Session = request.app.state.db_session_factory()

    try:
        logging.info(f"Forking a new session, id: {id(session)}")
        yield session
    finally:
        logging.info(f"Commiting the session, id: {id(session)}")
        session.commit()
        session.close()
