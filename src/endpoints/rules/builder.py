from typing import Dict, List, Tuple

from src.agent.actor import ActorLLM
from src.agent.template import SYSTEM_MESSAGE, TASK
from src.db.orms import DataSets
from src.estimator.estimator import RuleEstimator
from src.estimator.schemas import AgentResponse


class RulesBuilder:
    def __init__(self, version: str, rules_str: str):
        self.version = version
        self.rules_str = rules_str
        self.agent = ActorLLM(
            name="RulesBuilder",
            system_message=SYSTEM_MESSAGE.format(RULES=rules_str),
            llm_config={"model": "finaclegpt432k"},
            examples=None,
            functions_list=None,
            enable_cache=False,
            enable_logger=True,
        )

    def build(self, dataset: DataSets) -> Tuple[AgentResponse, List[Dict[str, str]]]:
        rules_data = self.agent.resolve_task(TASK.format(JSON_DATA=dataset.get_data_json_str()))
        if rules_data is None:
            return AgentResponse(response_string="", queries=[]), []
        agent_response = AgentResponse.perse_response(rules_data)
        estimated_results = RuleEstimator(queries=agent_response.queries).dry_estimate(dataset.data)
        return agent_response, estimated_results

    def get_chat_history(self) -> List[Dict[str, str]]:
        return self.agent.chat_history()
