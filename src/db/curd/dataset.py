import logging
from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from src.db.orms import DataSets

logger = logging.getLogger(__name__)


def get_datasets(db: Session, data_id: int) -> Optional[DataSets]:
    query_stmt = select(DataSets).where(DataSets.id == data_id)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching DataSets, for id: {data_id}, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched DataSets details for id: {data_id}",
        )
    return data


def get_datasets_by_version(db: Session, version: int) -> Sequence[DataSets]:
    query_stmt = select(DataSets).where(DataSets.version == version)
    status, data = None, []
    try:
        status = db.execute(query_stmt)
        data = status.scalars().all()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching DataSets, for version: {version}, Error - {e}",
        )
        data = []
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched DataSets for version : {version}",
        )
    return data


def get_latest_dataet(db: Session) -> Sequence[DataSets]:
    query_stmt = select(DataSets).order_by(DataSets.created_at.desc()).limit(1)
    status, data = None, []
    try:
        status = db.execute(query_stmt)
        data = status.scalars().all()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching DataSets, Error - {e}",
        )
        data = []
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched latest DataSets",
        )
    return data


def insert_datset(db: Session, insert_dict: dict) -> Optional[DataSets]:
    insert_dict_ = {
        **insert_dict,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    query_stmt = insert(DataSets).values(**insert_dict_).returning(DataSets)
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while inserting record DataSets, Error - {e}",
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully inserted DataSets id: {data.id}",
        )
    return data


def update_dataset(
    db: Session,
    update_dict: dict,
    data_id: int,
) -> Optional[DataSets]:
    update_dict_ = {**update_dict, "updated_at": datetime.now()}
    query_stmt = update(DataSets).where(DataSets.id == data_id).values(**update_dict_).returning(DataSets)
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while updating DataSets, for id: {data_id}, Error - {e}",
        )
        data = None
    else:
        logger.info(f"Session id {id(db)} | Sucessfully updated DataSets id: {data.id}")
    return data
