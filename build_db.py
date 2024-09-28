import logging
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists

import src.db.orms  # noqa: F401
from src.db.orms.base import meta
from src.settings import Settings

settings = Settings()

timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
logs_path = Path(settings.app.log_directory) / f"Database_init_Log_{timestamp}.log"

# Setting Looger Config

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler(logs_path, mode="w")],
)

logger = logging.getLogger(__name__)


def _create_database() -> None:
    logger.info("Creating Database .....")
    logger.info(f"DB URL {settings.db.db_url}")
    engine = create_engine(settings.db.db_url, echo=True)
    if not database_exists(engine.url):
        logger.info("Database not exists Creating a new one.....")
        create_database(engine.url)
    else:
        logger.info("Database exists .....")


def _create_schema() -> None:
    """Populates tables in the database."""
    logger.info("Creating Db Schama .....")
    logger.info(f"DB Schama {settings.db.db_schema}")
    if settings.db.db_schema is None:
        return
    engine = create_engine(settings.db.db_url, echo=True)

    with engine.begin() as connection:
        schema_exists = engine.dialect.has_schema(
            connection=connection,
            schema=settings.db.db_schema,
        )
        if not schema_exists:
            return_code = connection.execute(CreateSchema(settings.db.db_schema))
            logger.info(f"return_code {return_code}")
    engine.dispose()


def _create_tables() -> None:
    """Populates tables in the database."""
    logger.info("Creating Db Tables .....")
    logger.info(f"DB URL {settings.db.db_url}")
    engine = create_engine(settings.db.db_url, echo=True)

    with engine.begin() as connection:
        # return_code = connection.execute(meta.create_all, checkfirst=True)
        return_code = meta.create_all(connection, checkfirst=True)
        logger.info(f"return_code {return_code}")
    engine.dispose()


def one_time_activity() -> None:
    # _create_database()
    _create_schema()
    _create_tables()


if __name__ == "__main__":
    one_time_activity()
    # _create_database()
