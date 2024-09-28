import re
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class QueryDetails(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)
    description: str
    query: str


class QueryList(BaseModel):
    items: List[QueryDetails] = Field(default_factory=list)


class AgentResponse(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    response_string: str = Field(description="The response string to return to the user.")
    queries: List[QueryDetails] = Field(
        description="The queries that were executed to generate the response.",
        default_factory=list,
    )

    @property
    def is_empty(self) -> str:
        return self.response_string == "" or self.response_string is None

    @classmethod
    def perse_response(cls, data: str) -> "AgentResponse":
        if isinstance(data, dict):
            return data
        if not isinstance(data, str):
            raise ValueError("Response Shoule be valid Xml Format")
        try:
            pattern1 = r"<evaluation>(.*?)</evaluation>"
            pattern2 = r"<description>(.*?)</description>\s*<query>(.*?)</query>"
            queries = []
            matches = re.findall(pattern1, data, re.DOTALL)
            if not matches:
                raise ValueError("Response Shoule be valid Xml Format")
            for match in matches:
                sub_matches = re.findall(pattern2, match.strip(), re.DOTALL)
                item = [{"description": item[0].strip(), "query": item[1].strip()} for item in sub_matches]
                queries.extend(item)
        except Exception as err:
            raise err
        return cls(response_string=data, queries=queries)


class ChatMessage(BaseModel):
    role: str = Field(default="")
    content: str = Field(default="")


class ChatHistory(BaseModel):
    data: List[ChatMessage] = Field(default_factory=list)


class Version(BaseModel):
    major: int = Field(default=0)
    minor: int = Field(default=0)

    @classmethod
    def from_str(cls, version: str) -> "Version":
        major, minor = version.split(".")
        return cls(major=int(major), minor=int(minor))

    def to_str(self) -> str:
        return f"{self.major}.{self.minor}"

    def upadate_version(self) -> "Version":
        return Version(major=self.major, minor=self.minor + 1)

    def update_major_version(self) -> "Version":
        return Version(major=self.major + 1, minor=0)
