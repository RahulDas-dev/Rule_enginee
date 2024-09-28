from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, model_validator


class AppSettings(BaseModel):
    host: Optional[str] = "127.0.0.1"
    port: Optional[int] = 8000
    reload: bool = True
    debug: bool = True
    workers_count: int = 1
    log_directory: str = "logs"

    def __repr__(self) -> str:
        fields = "\n\t".join(f"{fld} = {getattr(self, fld)!r}" for fld in self.__annotations__)
        return f"{self.__class__.__name__}[\n\t{fields} \n]"

    @model_validator(mode="before")
    @classmethod
    def validate_setings(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError("Settings should be a dictionary object")
        log_directory = Path(data["log_directory"])
        if not log_directory.is_dir():
            raise ValueError("log_directory path not valid - {log_directory}")
        return data
