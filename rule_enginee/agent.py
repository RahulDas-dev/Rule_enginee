# %%
import os
import logging
import json
import re
from typing import List, Dict, Any, Optional

from jsonata import Jsonata
from litellm import completion, stream_chunk_builder
from termcolor import colored

from src.transformer import XmlLoader, RemovePrefix

# %%
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# %%
os.environ["AZURE_API_KEY"] = "8770a68132394ac489e5134f93ecf2f8"
os.environ["AZURE_API_BASE"] = (
    "https://az-usw-openai-globalaisolutions.openai.azure.com/"
)
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"
os.environ["http_proxy"] = "http://10.68.4.61:80"
os.environ["https_proxy"] = "http://10.68.4.61:80"
# os.environ['LITELLM_LOG'] = 'DEBUG'

os.environ["VERTEXAI_PROJECT"] = "finacle-analytics"
os.environ["VERTEXAI_LOCATION"] = "us-east5"
DEFAULT_CONFIG = {"temperature": 0.2, "timeout": 600, "max_tokens": 5000}

# %%
config2 = {"model": "azure/finaclegpt432k"}
config2 = {"model": "azure/finaclegpt4o", "max_tokens": 4096}
config = {"model": "vertex_ai/claude-3-opus@20240229"}

# %%
data_path = "./data/SampleCreditReports/1af3f6c9-9010-4aa2-9488-7f54165f2dee.html"

loder = XmlLoader.from_path(data_path)

documents = RemovePrefix().transform(loder.document)

json_data = json.dumps(documents, indent=4)

# %%
RULES = """
1. Score < 650 THEN Reject
      Rule: If the credit score is less than 650, the applicant is rejected.
2. More than 2 PAN IDs THEN Reject
      Rule: If there are more than two PAN IDs, the applicant is rejected.
3. TotalInquiries > 3 THEN Reject
      Rule: If the number of total inquiries exceeds 3, the applicant is rejected.
4. if any Account of AccountType Excluding Credit Cards
      a. SuitFiledStatus = Yes THEN Reject
      Rule: If any Account has a "Suit Filed" status as "Yes", the applicant is rejected.
      b. WriteOffAmount > 0 THEN Reject
      Rule: If any Account has a WriteOffAmount greater than 0, the applicant is rejected.
      c. PastDueAmount > 1,500 and DateReported < 12 months THEN Reject
      Rule: If any Account has a PastDueAmount greater than 1,500, and DateReported is within the last 12 months and the PaymentStatus in any of the past 12 months is one of the listed delinquency statuses, the applicant is rejected.
      d. AccountStatus in {WDF, SUB, DBT, etc.} THEN Reject
      Rule: If any account has a status in the listed statuses, the applicant is rejected.
      e. PastDueAmount > 1,500 and DateReported > 12 months THEN Reject
      Rule: If any Account has a PastDueAmount greater than 1,500, DateReported is more than 12 months ago, and PaymentStatus in any of the past 6 months indicates delinquency, the applicant is rejected.
5. if any Account of AccountType = Credit Card  and PastDueAmount > 5,000 THEN Reject
      Rule: If any credit card account has a PastDueAmount greater than 5,000, the applicant is rejected.
"""

system_msg = f"""
Hi, as an AI model, you are well-versed with JSON data and JSON Query Language [Jsonata].       
Your task is to help build a Rule Engine on JSON Data using JSON Query Language.   
The final output will be 'Rejected' or 'Not Rejected' based on the following rules:    
  
# Rules     
{RULES}

# Self Reflection
Before generating the JSON queries, reflect on the rules definition, and the given example data.  
1. Reflect on the Example data and the associated Query Attribute and understand the corresponding Schemas for the targeted Attribute.  
2. List down the attributes and their type, which are mentioned in the rule definitions.  
3. Kindly reflect on the type of data, List Down the attributes that needs to Type casted in order to perform any comprison or boolean oerations.
  
# How To 
Once Self Reflection is complete you can proceed to create a set of JSON queries using JSON Query Language [Jsonata] inorder to evaluate the rules. Kindly
Strictly follow the bellow Guidelines-
1. All the evaluation logic should be written using JSON Query Language[Jsonata]. It should be strictly in JSON Query Language[Jsonata], no other languages are allowed.  
2. Kindly reflect on the Type of data, if needed convert the data into sutaitble type before doing any comparison or other operations.
3. Ensure every JSON Query evaluates to 'Rejected' or 'Not Rejected'. Remember, it should be strictly 'Rejected' or 'Not Rejected', no other formats are allowed.  
   
# The Code Bellow shows The end-to-end logic how user will be using the Json Queries -  
   
```python  
from jsonata import Jsonata   
  
# Generate JSON Query from AI Agent  
query_list = call_the_agent()  
   
result = None  
for query in query_list:   
    expr = Jsonata(query)  
    result = expr.evaluate(documents)  
    if result == 'Rejected':  
        break  
          
print(result)          
```  
Users will evaluate the queries using the Jsonata Package , Hence it is extremely important to use JSON Query Language [Jsonata]  

# Expected Output Format - 
Each Rule item will be having two componnets - Descrption of the Json Query and the Query String. 
Ensure the output always follows the given XML format:  

<evaluation>    
    <jsonqry>    
        <description> Describe Rule1 here ...</description>    
        <query>This should contain the JSON Query string only ...</query>    
    </jsonqry>    
    <jsonqry>    
        <description> Describe Rule2 here ...</description>    
        <query>This should contain the JSON Query string only ...</query>    
    </jsonqry>    
    ...    
</evaluation> 
"""

sytem_reminder_msg = """
All the Rules evaluation logic should be written using JSON Query Language. It Should be strictly in Json Query language, No other Lanugages are allowed .
# Expected Output Format -  
Kindly make Sure the output will be always given folowing xml format
<evaluation>  
    <jsonqry>  
        <description> Describe Rule1 here ...</description>  
        <query>This should contain the JSON Query string only ...</query>  
    </jsonqry>  
    <jsonqry>  
        <description> Describe Rule2 here ...</description>  
        <query>This should contain the JSON Query string only ...</query>  
    </jsonqry>  
    ...  
</evaluation>
"""

# %%
messages = [
    {
        "role": "system",
        "content": system_msg,
    },
    {
        "role": "user",
        "content": f" Here is the one example Json data Kindly think step by step and Generate JSON Query for Data Transformation and Rule Evalutaions, \n {json_data}",
    },
]

sys_rem_msg = [{"role": "system", "content": sytem_reminder_msg}]

messages = messages + sys_rem_msg

# %%
response = completion(model=config2["model"], stream=True, messages=messages)

print(response)
chunks = []
for chunk in response:
    # print(type(chunk))
    chunks.append(chunk)
    chunk_var = chunk.choices[0].delta
    if chunk_var.get("content", None) is not None:
        print(colored(chunk_var["content"], "green"), end="", flush=True)
    else:
        pass
message_final = stream_chunk_builder(chunks, messages=messages)

# %%
response = message_final.choices[0].message.content


# %%
def mather(text: str) -> List[Dict[str, Any]]:
    pattern = re.compile(
        r"<description>(.*?)</description>\s*<query>(.*?)</query>", re.DOTALL
    )
    matches = pattern.findall(text)
    if matches is None:
        return []
    else:
        result = [
            {"description": match[0].strip(), "query": match[1].strip()}
            for match in matches
        ]
        return result


def extract_transformations(response: str) -> Optional[str]:
    try:
        # pattern1 = r"<transformation>(.*?)</transformation>"
        pattern2 = r"<evaluation>(.*?)</evaluation>"
        items1, items2 = [], []
        # match1 = re.findall(pattern1, response, re.DOTALL)
        # for match in match1:
        #    item = mather(match.strip())
        #    items1.extend(item)
        match2 = re.findall(pattern2, response, re.DOTALL)
        for match in match2:
            item = mather(match.strip())
            items2.extend(item)
    except Exception as err:
        logger.error(f"Error While output Persing Kindly Check {err}")
        items1, items2 = [], []
    finally:
        return items1, items2


# %%
items1, items2 = extract_transformations(response)

# %%
items2

# %%
for index, item in enumerate(items2):
    query = item.get("query", None)
    if query is None:
        continue
    try:
        expr = Jsonata(query)
        result = expr.evaluate(documents)
        print(f"{index} ->{query} ->{result}")
    except Exception as e:
        print(f"{index} ->{query} ->{e}")

# %%
qry = items2[0].get("query", None)
print(qry.strip())
expr = Jsonata(query)
result = expr.evaluate(documents)

# %%
import jsonata

# JSON data
data = {"Score": {"Value": "600"}}

# Jsonata query
query = """
(
  $score := $number(Score.Value);
  $score < 650 ? "Rejected" : "Not Rejected"
)
"""

# Evaluate the query
expr = jsonata.Jsonata(query)
result = expr.evaluate(data)

print(result)  # Output: "Rejected"

# %%
