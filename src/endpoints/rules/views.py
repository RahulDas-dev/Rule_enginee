import logging
from typing import Mapping

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import UJSONResponse
from sqlalchemy.orm import Session

from src.db.curd.dataset import get_latest_dataet
from src.db.curd.rules_info import get_latest_rules_info, insert_actions_info
from src.db.provider import get_db_session
from src.endpoints.rules.builder import RulesBuilder
from src.endpoints.rules.schemas import RequestBody, ResponseBody
from src.estimator.schemas import Version

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/latest_vesion", response_model=ResponseBody)
def latest_vesion(session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    latest_rules = get_latest_rules_info(session)
    curent_version = "1.0" if latest_rules is None else latest_rules.version
    rules_str = "" if latest_rules is None else latest_rules.rules_str
    next_version = [
        Version.from_str(curent_version).upadate_version().to_str(),
        Version.from_str(curent_version).update_major_version().to_str(),
    ]
    content_ = {
        "version": curent_version,
        "next_versions": next_version,
        "rules_str": rules_str,
    }
    return UJSONResponse(status_code=status.HTTP_200_OK, content=content_)


@router.post("/new/", status_code=status.HTTP_201_CREATED)
def new(reqwstbdy: RequestBody = Body(), session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    logger.info(f"Session id: {id(session)} | Request body: {reqwstbdy.version} ")
    dataset = get_latest_dataet(session)
    if len(dataset) == 0:
        logger.error(f"Session id: {id(session)} | No datasets Found")
        return UJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=[{"query": "None", "error": "No datasets Found"}],
        )

    rules_builder = RulesBuilder(reqwstbdy.version, reqwstbdy.rules_str)
    response, estimated_score = rules_builder.build(dataset[0])
    if response.is_empty:
        return UJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=estimated_score)
    has_error = any(True for item in estimated_score if item.get("error", None) is not None)
    if has_error:
        return UJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=estimated_score)
    insert_dict = {
        "version": reqwstbdy.version,
        "rules_input": reqwstbdy.rules_str,
        "agent_reponse": response.response_string,
        "querys": response.queries,
        "agent_chat_history": rules_builder.get_chat_history(),
        "status": "Success",
        "retry_count": 1,
    }
    action_info = insert_actions_info(session, insert_dict)
    if action_info is None:
        logger.error(f"Session id: {id(session)} | Action Creation Failed")
    return UJSONResponse(
        status_code=(status.HTTP_400_BAD_REQUEST if action_info is None else status.HTTP_201_CREATED),
        content=estimated_score,
    )
