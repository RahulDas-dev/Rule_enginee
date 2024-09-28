from pathlib import Path
from typing import Any, Literal, Optional

from pydantic import BaseModel, model_validator
from sqlalchemy import URL

Dbtypes = Literal["SQLITE", "POSTGRES", "MYSQL"]


class DbSettings(BaseModel):
    kind: Dbtypes = "POSTGRES"
    host: Optional[str] = "10.73.41.9"
    port: Optional[int] = 5432
    username: Optional[str]
    password: Optional[str]
    db_schema: Optional[str]
    db_name: Optional[str]
    db_logger: bool = False

    def __repr__(self) -> str:
        fields = "\n\t".join(f"{fld} = {getattr(self, fld)!r}" for fld in self.__annotations__)
        return f"{self.__class__.__name__}[\n\t{fields} \n]"

    @model_validator(mode="before")
    @classmethod
    def validate_setings(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError("DB Settings should be a dictionary object")
        if data["kind"] == "SQLITE":
            db_file_path = Path(Path.cwd()) / str(data["db_name"])
            if db_file_path.parent.exists():
                data["host"] = None
                data["port"] = None
                data["user"] = None
                data["password"] = None
                data["db_schema"] = None
            else:
                raise ValueError("Sqlite DB path not valid")
        return data

    @property
    def db_url(self) -> URL:
        """Assemble database URL from settings.

        :return: database URL.
        """
        if self.kind == "SQLITE":
            url = URL.create(
                drivername="sqlite",
                database=self.db_name,
            )
        elif self.kind == "POSTGRES":
            url = URL.create(
                drivername="postgresql",
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db_name,
            )
        elif self.kind == "MYSQL":
            url = URL.create(
                drivername="mysql+pymysql",  # For "mysql+asyncmy",
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db_name,
            )
        elif self.kind == "ORACLE":
            url = URL.create(
                drivername="oracle",  # For "mysql+asyncmy",
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.db_name,
            )
        return url
