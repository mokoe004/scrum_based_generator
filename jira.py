# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
from logger_config import setup_logger

logger = setup_logger("JiraLogger", "jira.log")

url = "https://stud-team-s8gnf6oc.atlassian.net/rest/api/2/issue"

auth = HTTPBasicAuth(
    "mohammad.koese002@stud.fh-dortmund.de", 
    "ATATT3xFfGF0_SrvXBqizrgCKo_fHdRS51Y0Gmue0RJildZfL1s2QpJSDLgVx-QdL5ng_FXyY9YyWBBBWHNCBY4YOjQQGXiaKKsVH1dKcRojxhebu_oxlOpFKUq2UH-AbEEP2CqOZix9YSEwuUW23gK0XWg3029vvPE8ofSQQ_Wy04rtIejudOg=BDCABA40"
    )

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

def get_issue_type(project_key):
    url = f"https://stud-team-s8gnf6oc.atlassian.net/rest/api/2/issue/createmeta/{project_key}/issuetypes"
    response = requests.get(
        url,
        headers=headers,
        auth=auth,
    )
    logger.info(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def create_issue(summary, user_story):
    payload = json.dumps({
        "fields": {
        "project": {
                "key": "SCRUM"
            },
        "summary": summary,
        "description": user_story,
        "issuetype": {
            "name": "Story"
        },
    }
    })
    response = requests.post(
    url,
    data=payload,
    headers=headers,
    auth=auth,
    )
    logger.info(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
