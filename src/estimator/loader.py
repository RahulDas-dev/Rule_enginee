import json
import logging
from typing import Any, OrderedDict

import xmltodict

logger = logging.getLogger(__name__)


class XmlLoader:
    def __init__(self, document: OrderedDict[str, Any]):
        self._document = document

    @property
    def document(self) -> OrderedDict[str, Any]:
        return self._document

    @classmethod
    def from_path(cls, data_path: str) -> "XmlLoader":
        try:
            with open(data_path, "rb") as file:
                document = xmltodict.parse(file)
            document = (
                document.get("soapenv:Envelope", {})
                .get("soapenv:Body", {})
                .get("sch:InquiryResponse", {})
                .get("sch:ReportData", {})
            )
        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            document = None
        return cls(document)

    @classmethod
    def from_content(cls, content: str) -> "XmlLoader":
        try:
            document = xmltodict.parse(content)
            document = (
                document.get("soapenv:Envelope", {})
                .get("soapenv:Body", {})
                .get("sch:InquiryResponse", {})
                .get("sch:ReportData", {})
            )
        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            document = None
        return cls(document)

    def save_as_json(self, path: str) -> None:
        with open(path, "w") as outfile:
            json.dump(self._document, outfile, indent=4)
