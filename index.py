import generator, json, jira, create_project
from logger_config import setup_logger
import time

logger = setup_logger("IndexLogger", "index.log")

user_stories_path = (
    "./output/user_stories.json"
)
tasks_path = ("./output/tasks.json")
package_design_path = ("output/package_design.json")
prompt_path = ("./prompt_demo.json")
code_path = ("./output/code.json")


def read_prompt_json(filepath) -> dict:
    with open(filepath, "r") as file:
        prompt = json.load(file)
        logger.info("Prompt read successfully.")
        return prompt


def get_pVision() -> str:
    pVision = read_prompt_json(prompt_path)["product_vision"]
    prompt_string = f"""
                    For {pVision['target_group']} with {pVision['problem']}, {pVision['product_name']} is a {pVision['product_type']}, that {pVision['key_features']}.
                    Unlike {pVision['competitor']}, {pVision['product_name']} provides {pVision['unique_benefit']}.
                    """
    logger.info("Prompt converted to string successfully.")
    return prompt_string

# Save artifacts to file, can be user stories or tasks. 
def save_as_json(pData, filepath):
    with open(filepath, "r+") as file:
        data = json.load(file)
        data = pData
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        logger.info(f"{filepath} saved successfully in file.")

def main():
    #tasks = read_prompt_json(tasks_path)
    #epics = read_prompt_json(user_stories_path)
    #package_design = read_prompt_json(package_design_path)
    #code = read_prompt_json(code_path)
    pvision = read_prompt_json(prompt_path)["product_vision"]
    personas = generator.generate_personas(pvision, 5)
    logger.info("Personas generated successfully.")
    epics = generator.generate_epics(pvision, personas)
    time.sleep(60)
    logger.info("Epics generated successfully.")
    for epic in epics:
        userStories = generator.generate_user_storys(pvision, personas, epic)
        logger.info("User stories generated successfully.")
        epic["user_stories"] = userStories
        time.sleep(30)
    save_as_json(epics, user_stories_path)
    time.sleep(30)
    tasks = generator.generate_tasks(epics)
    save_as_json(tasks, tasks_path)
    time.sleep(30)
    package_design = generator.generate_package_design(tasks, epics, pvision)
    # save_as_json(package_design, package_design_path)
    # time.sleep(30)
    # code = generator.generate_code(tasks, pvision, package_design)
    # save_as_json(code, code_path)
    # create_project.create(code)

if __name__ == "__main__":
     main()


# # Funktion zum Konvertieren von JSON-Daten in Jira-kompatibles Markdown
# def convert_to_jira_markdown(data):
#     # User Story
#     markdown = f"*User Story:*\n_{data['userStory']}_\n\n"

#     # Acceptance Criteria
#     markdown += "*Acceptance Criteria:*\n"
#     for criterion in data["acceptanceCriteria"]:
#         markdown += f"- {criterion}\n"

#     # Persona
#     markdown += "\n*Persona:*\n"
#     for key, value in data["persona"].items():
#         markdown += f"- **{key.capitalize()}:** {value}\n"

#     logger.info("User stories converted to Jira markdown successfully.")
#     return markdown


# def create_jira_issues(data):
#     for story in data:
#         summary = story["userStory"]
#         description = convert_to_jira_markdown(story)
#         jira.create_issue(summary, description)
#     logger.info("Jira issue created successfully.")


# prompt = read_prompt_json()
# userStories = genai.generate_user_storys(prompt)
# userStories = json.loads(userStories)
# logger.info("User stories generated successfully.")
# Create Jira issues
# create_jira_issues(userStories)
