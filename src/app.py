# from importlib import metadata
import json
import logging
from typing import Callable

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import UJSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.loggers import set_up_loggers
from src.routers import api_router
from src.settings import Settings

settings = Settings()
set_up_loggers(settings)

logger = logging.getLogger(__name__)

loading_status = load_dotenv(verbose=True)
logger.info(f"loading_status - {loading_status}")


def setup_database(app: FastAPI) -> None:  # pragma: no cover
    """Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """

    def _custom_json_serializer(*args, **kwargs) -> str:
        """Encodes json in the same way that pydantic does."""
        # return json.dumps(*args, default=pydantic.json.pydantic_encoder, **kwargs)
        return json.dumps(*args, default=jsonable_encoder, **kwargs)

    engine = create_engine(
        settings.db.db_url,
        echo=settings.db.db_logger,
        json_serializer=_custom_json_serializer,
    )
    session_factory = sessionmaker(engine, expire_on_commit=False, autoflush=True)
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


def register_startup_event(app: FastAPI) -> Callable[[], Callable]:  # pragma: no cover
    """Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """
    logger.info("Adding listener for the startup event")

    def _startup() -> None:
        app.middleware_stack = None
        setup_database(app)
        app.middleware_stack = app.build_middleware_stack()

    app.add_event_handler("startup", _startup)
    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Callable]:  # pragma: no cover
    """Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """
    logger.info("Adding listener for the shutdown event")

    def _shutdown() -> None:
        app.state.db_engine.dispose()

    app.add_event_handler("shutdown", _shutdown)
    return _shutdown


def setup_application() -> FastAPI:
    app = FastAPI(
        title="Credit Score Backend Sevicess",
        # version=metadata.version("backend"),
        docs_url=None if settings.is_production else "/docs",
        redoc_url=None if settings.is_production else "/redoc",
        openapi_url=None if settings.is_production else "/openapi.json",
        default_response_class=UJSONResponse,
        debug=False,
    )
    register_startup_event(app)
    register_shutdown_event(app)
    # Add Middle Wires.
    # Main router for the API.
    app.include_router(router=api_router)
    return app


app = setup_application()
