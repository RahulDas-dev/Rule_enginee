import logging
from datetime import datetime
from typing import Optional
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from ..orms.rules_info import RulesInfo

logger = logging.getLogger(__name__)


def get_rules_info(db: Session, rules_id: int) -> Optional[RulesInfo]:
    query_stmt = select(RulesInfo).where(RulesInfo.id == rules_id)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching RulesInfo, for id: {rules_id}, Error - {e}"
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched RulesInfo details for id: {rules_id}"
        )
    finally:
        return data


def get_rules_info_by_version(db: Session, rules_version: int) -> Optional[RulesInfo]:
    query_stmt = select(RulesInfo).where(RulesInfo.version == rules_version)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while fetching RulesInfo, for version: {rules_version}, Error - {e}"
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully fetched RulesInfo for version : {rules_version}"
        )
    finally:
        return data


def insert_actions_info(db: Session, insert_dict: dict) -> Optional[RulesInfo]:
    insert_dict_ = {
        **insert_dict,
        **{"created_at": datetime.now(), "updated_at": datetime.now()},
    }
    query_stmt = insert(RulesInfo).values(**insert_dict_).returning(RulesInfo)
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while inserting record RulesInfo, Error - {e}"
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully inserted RulesInfo id: {data.id}"
        )
    finally:
        return data


def update_actions_info(
    db: Session, update_dict: dict, rules_id: int
) -> Optional[RulesInfo]:
    update_dict_ = {**update_dict, **{"updated_at": datetime.now()}}
    query_stmt = (
        update(RulesInfo)
        .where(RulesInfo.id == rules_id)
        .values(**update_dict_)
        .returning(RulesInfo)
    )
    status, data = None, None
    try:
        with db.begin():
            status = db.execute(query_stmt)
            data = status.scalars().one()
    except Exception as e:
        db.rollback()
        logger.error(
            f"Session id {id(db)} | Error while updating RulesInfo, for id: {rules_id}, Error - {e}"
        )
        data = None
    else:
        logger.info(
            f"Session id {id(db)} | Sucessfully updated actions_info id: {data.id}"
        )
    finally:
        return data
