from fastapi import UploadFile
from pydantic import BaseModel, Field


class RequestBody(BaseModel):
    version: str = Field(description="Version of the rules")
    file: UploadFile = Field(description="Rules in string format")
