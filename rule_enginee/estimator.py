import logging
from typing import Any, Dict, List, Optional
from .response import QueryDetails
from jsonata import Jsonata

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
        finally:
            return failure_reason

    def dry_run(self, data: Dict[str, Any]):
        results = []
        for item in self.queriesinfo:
            try:
                expr = Jsonata(item.query)
                status = expr.evaluate(data)
                logger.info(f"Rule: {item.query}, Result: {status}")
                results.append({"query": item.query, "status": status})
            except Exception as e:
                logger.error(f"Error while evaluating rule: {item.query}")
                logger.error(f"Error details: {e}")
                results.append({"query": item.query, "status": status})
        return results
