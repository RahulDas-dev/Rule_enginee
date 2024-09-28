import json
import logging
import os

from dotenv import load_dotenv

from src.agent.actor import ActorLLM
from src.estimator import RemovePrefix, XmlLoader

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
    # format="%(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

loading_status = load_dotenv(verbose=True)

logger = logging.getLogger(__name__)

logger.info(f"loading_status {loading_status}")

data_path = "./data/sample/1af3f6c9-9010-4aa2-9488-7f54165f2dee.html"

loder = XmlLoader.from_path(data_path)

documents = RemovePrefix().transform(loder.document)

JSON_DATA = json.dumps(documents, indent=4)
# print(JSON_DATA)

# sys_msg = SYSTEM_MESSAGE.format(RULES=RULES)
sys_msg = "You Are Helpfull AI Assistant"

task = f"Here is the one example Json data Kindly think step by step and Generate JSON Query for Data Transformation and Rule Evalutaions, \n {JSON_DATA}"  # noqa: E501
task = "What is the JSON Query Language ?"

os.environ["LITELLM_LOG"] = "DEBUG"

config3 = {"model": "finaclegpt432k"}
config2 = {"model": "finaclegpt4o", "max_tokens": 4096}
config1 = {"model": "claude-3-opus@20240229"}

agent = ActorLLM(name="QueryBuilder", system_message=sys_msg, llm_config=config3)

agent.resolve_task(task)
