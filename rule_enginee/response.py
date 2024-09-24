from typing import Dict, List, Any
import re
from pydantic import BaseModel, ConfigDict, Field


class QueryDetails(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)
    description: str
    query: str


class Response(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)

    response_string: str = Field(
        description="The response string to return to the user."
    )
    queries: List[QueryDetails] = Field(
        description="The queries that were executed to generate the response."
    )

    @classmethod
    def perse_response(cls, data: str) -> Dict[str, Any]:
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
                item = [
                    {"description": item[0].strip(), "query": item[1].strip()}
                    for item in sub_matches
                ]
                queries.extend(item)
        except Exception as err:
            raise ValueError(err.message)
        finally:
            return cls(response_string=data, queries=queries)
