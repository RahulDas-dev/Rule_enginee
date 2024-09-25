import logging
import json

from dotenv import load_dotenv

from rule_enginee import XmlLoader, RemovePrefix
from rule_enginee.agent.actor import ActorLLM

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

task = f"Here is the one example Json data Kindly think step by step and Generate JSON Query for Data Transformation and Rule Evalutaions, \n {JSON_DATA}"
task = "What is the JSON Query Language ?"

# os.environ["LITELLM_LOG"] = "DEBUG"

config3 = {"model": "gpt432k"}

agent = ActorLLM(name="QueryBuilder", system_message=sys_msg, llm_config=config3)

agent.resolve_task(task)
