from typing import Tuple

from pydantic import BaseModel, Field


class RequestBody(BaseModel):
    version: str = Field(description="Version of the rules")
    rules_str: str = Field(description="Rules in string format")


class ResponseBody(BaseModel):
    version: str = Field(description="Current version of the rules")
    reules_str: str = Field(description="Rules in string format")
    next_versions: Tuple[str, str] = Field(description="Next versions of the rules")
