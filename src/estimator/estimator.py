import logging
from typing import Any, Dict, List, Optional

from jsonata import Jsonata

from .schemas import QueryDetails

logger = logging.getLogger(__name__)


class RuleEstimator:
    def __init__(self, queries: List[QueryDetails]):
        self.queriesinfo = queries

    def estimate(self, data: Dict[str, Any]) -> Optional[str]:
        failure_reason = None
        try:
            for item in self.queriesinfo:
                expr = Jsonata(item.query)
                status = expr.evaluate(data)
                logger.info(f"Rule: {item.query}, status: {status}")
                if status == "Rejected":
                    failure_reason = item.description
                    break
        except Exception as e:
            logger.error(f"Error while evaluating query: {item.query}")
            logger.error(f"Error details: {e}")
            failure_reason = f"Error: {e}"
        return failure_reason

    def dry_estimate(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        results = []
        for idex, item in enumerate(self.queriesinfo):
            try:
                expr = Jsonata(item.query)
                status = expr.evaluate(data)
                if status is None:
                    logger.error(f"{idex+1}. Error while evaluating rule: {item.query} Error details: Invalid status")
                    results.append({"query": item.query, "error": "Invalid status: {status}"})
                elif isinstance(status, str) and (status.lower() in ["rejected", "not rejected"]):
                    logger.info(f"{idex+1}. Rule: {item.query}, Result: {status}")
                    results.append({"query": item.query, "status": status})
                else:
                    logger.error(f"{idex+1}. Error while evaluating rule: {item.query} Error details: Invalid status")
                    results.append({"query": item.query, "error": "Invalid status: {status}"})
            except Exception as e:
                logger.error(f"{idex+1}. Error while evaluating rule: {item.query} Error details: {e}")
                results.append({"query": item.query, "error": str(e)})
        return results
