from pydantic import BaseModel, Field


class ProjectBody(BaseModel):
    project_id: int
    flow: str = Field(default="")
    page: str = Field(default="")
