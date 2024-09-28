import json
import logging
from typing import Mapping

from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.orm import Session

from src.db.curd.dataset import insert_datset
from src.db.provider import get_db_session
from src.estimator.loader import XmlLoader
from src.estimator.remove_prefix import RemovePrefix

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/new/", status_code=status.HTTP_201_CREATED)
def new(version: str, file: UploadFile, session: Session = Depends(get_db_session)) -> Mapping[str, str]:
    logger.info(f"Session id: {id(session)} | filename: {file.filename} ")
    json_data = None
    try:
        file_content = file.file.read()
        loder = XmlLoader.from_content(file_content.decode("utf-8"))
        documents = RemovePrefix().transform(loder.document)
        json_data = json.dumps(documents, indent=4)
    except Exception as e:
        logger.error(f"Error while loading data: {e}")
        json_data = {}
        message = "Error while loading data"
    else:
        metadata = {
            "name": file.filename,
            "extn": file.filename.split(".")[-1],
        }
        inser_dict = {
            "version": version,
            "dmetadata": metadata,
            "dformat": file.filename.split(".")[-1],
            "data": json_data,
        }
        insert_datset(session, inser_dict)
        message = "Rule created successfully"
    return {"message": message}
