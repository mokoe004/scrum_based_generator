import os, json
from typing import Any, List, Optional
from pydantic import BaseModel, Field

from logger_config import setup_logger
from models.user_storys import EpicListModel, PersonaListModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSerializable

logger = setup_logger("GeneratorLogger", "generator.log")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", api_key=os.environ.get("GOOGLE_API_KEY")
)

def generate_personas(pVision, personas_amount):
    prompt_in = f"""
                                You are a project owner, responsible for creating personas for a new project. 
                                Generate {personas_amount} personas for the following project. 
                                Provide only the personas in JSON as output.

                                Generate {personas_amount} personas for the following project, discribed with the Product vision. 
                                Ensure that each persona is distinct, with detailed attributes based on the project vision. 
                                Each persona should be unique in terms of background, motivation, and goals. Try to cover a diverse range of potential users.
                                For each persona, consider the following attributes and context. Follow a step-by-step thought process to carefully define each aspect:\n\n

                                Product vision: {pVision}\n\n
                                
                                1. Name: Choose a realistic and contextually appropriate name based on the demographics and market segment.
                                2. Age: Consider the typical age range of individuals relevant to the project vision.
                                3. Occupation: Identify a profession that aligns with the project's goals and the persona's motivations.
                                4. Background: Detail the persona’s background, including education, experience, and personal life. Think about how this background influences their interactions with the product or service.
                                5. Motivation: What drives this persona? What are their personal or professional motivations in relation to the project vision? Be specific in connecting their motivations to the project.
                                6. Goal: Define the persona’s main goal when interacting with the product or service. Consider how their objectives may differ depending on their role or background.

                                Each persona should reflect a different aspect of the target audience, ensuring diversity in background, motivation, and goals. 

                                """

    parser = JsonOutputParser(pydantic_object=PersonaListModel)
    prompt = PromptTemplate(
        template=prompt_in,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    response = generate_valid_json(chain)
    logger.info("Personas generated successfully.")
    return response


def generate_user_storys_and_epics(pVision: str, personas: dict):
    prompt_in = f"""
                                You are a project owner, responsible for creating user stories and epics for a new project. 
                                Generate User Storys and Epics, based on the Product Vision and the Personas.
                                Always use the persona as the subject of the user story and for each Persona one User Story. 
                                Provide only the user stories and epics in JSON as output.

                                Generate Epics and User Stories based on the following Personas and Product Vision. Ensure that each Epic contains a clear business value and that User Stories follow the format: "As a [Persona], I want to [Goal], so that [Benefit]." 

                                Important Guidelines:
                                1. Persona Selection: The actor for each User Story must be one of the predefined personas listed below.
                                2. Business Value: Each Epic must have a clear business value that aligns with the overall product vision.
                                3. No Acceptance Criteria: Do not include acceptance criteria for either Epics or User Stories.
                                4. Realistic Goals: The goals in the User Stories must be achievable and grounded, as they will serve as the basis for small-scale code generation.
                                5. Output Format: Return the result in valid JSON format, with Epics and their corresponding User Stories.

                                Personas: {personas.__str__} \n\n
                                Product Vision: {pVision} \n\n

                """
    parser = JsonOutputParser(pydantic_object=EpicListModel)
    prompt = PromptTemplate(
        template=prompt_in,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    response = generate_valid_json(chain)
    logger.info("User stories and epics generated successfully.")
    logger.info(response)
    return response


def generate_acceptance_criteria(userStory: dict):
    prompt_in = f"""
                                You are a project owner, responsible for creating acceptance criteria for user stories. 
                                Generate acceptance criteria for the following user stories. 
                                Provide only the acceptance criteria in JSON as output.

                                Generate between 3 and 8 acceptance criteria for the following user story. 
                                Ensure that the acceptance criteria are specific, measurable, and achievable. 
                                Provide only the acceptance criteria as an python array as output. 
                                For the following User Stories provided in JSON format, generate between 3 and 8 acceptance criteria for each. The acceptance criteria should be clear, measurable, and focused on what the system needs to achieve rather than how it is implemented. Follow these best practices when creating the criteria:
                                
                                User Story: {userStory} \n\n

                                1. Clarity: Ensure that each acceptance criterion is specific and easy to understand.
                                2. Measurability: The criteria must be testable and verifiable, either through automated tests or manual review.
                                3. Focus on the outcome: The criteria should describe what the system needs to do, not how to do it.
                                4. Edge Cases: Consider edge cases and negative scenarios where the system might fail or need to handle errors gracefully.
                                5. User Perspective: Write the acceptance criteria from the personas perspective of the user story, focusing on their interactions and expectations.
                                6. Success Conditions: Define what constitutes success for each user story, including any conditions for completing the feature.
                """
    parser = JsonOutputParser(pydantic_object=List[str])
    prompt = PromptTemplate(
        template=prompt_in,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    response = generate_valid_json(chain)
    logger.info("Acceptance criteria generated successfully.")
    return response


def generate_tasks(userStory: dict):
    prompt_in = f"""
                                You are a project owner, responsible for creating tasks for user stories. 
                                Generate tasks for the following user stories. 
                                Provide only the tasks in JSON as output.

                                Generate tasks for the following user story. 
                                Ensure that the tasks are specific, actionable, and focused on the implementation details. 
                                Provide only the tasks as an python array as output. 
                                For the following User Stories provided in JSON format, generate tasks. The tasks should be clear, actionable, and focused on the steps needed to implement the user story. Follow these best practices when creating the tasks:

                                User Story: {userStory} \n\n

                                1. Specificity: Each task should be specific and focused on a single action or goal.
                                2. Actionable: The tasks should be actionable and clearly defined, with a clear outcome or result.
                                3. Implementation Details: Focus on the steps needed to implement the user story, rather than high-level goals.
                                4. Dependencies: Consider any dependencies or prerequisites for each task, including external services or resources.
                                5. Testability: Ensure that each task can be tested and verified, either through automated tests or manual review.
                                6. Priority: Assign a priority or order to the tasks based on their importance and impact on the user story.
                                        """
    parser = JsonOutputParser(pydantic_object=List[str])
    prompt = PromptTemplate(
        template=prompt_in,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    response = generate_valid_json(chain)
    logger.info("Tasks generated successfully.")
    return response.text


def create_backlog(userStorys: dict):
    """
    Generate a backlog for the given user stories. Prioritize the user stories based on their importance and dependencies,
    by sorting them in the order they should be implemented within the array.

    Args:
    userStorys (dict): The user stories to generate the backlog for.
    """
    prompt_in = f"""
                                You are a project owner, responsible for creating a backlog for user stories. 
                                You should only do the prioritization of the user stories based on their importance and dependencies.
                                Provide only the backlog in JSON as output.

                                Generate a backlog for the following user stories. 
                                Prioritize the user stories based on their importance and dependencies, 
                                by sorting them in the order they should be implemented within the array. 
                                Provide only the backlog as an python array as output. 

                                User Storys: {userStorys} \n\n

                                1. Importance: Consider the business value and impact of each user story on the overall project goals.
                                2. Dependencies: Identify any dependencies between user stories that may affect the order of implementation.
                                3. Complexity: Evaluate the complexity and effort required to implement each user story.
                                4. Priority: Assign a priority to each user story based on its importance and dependencies.
                                5. Order: Sort the user stories in the array based on their priority and dependencies.
                                        """
    parser = JsonOutputParser(pydantic_object=List[str])
    prompt = PromptTemplate(
        template=prompt_in,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    response = generate_valid_json(chain)
    logger.info("Backlog generated successfully.")
    return response.text


def generate_package_design(tasks: dict, userStorys: dict, pVision: str):
    prompt_in = f"""
                                You are a project owner, responsible for creating a package design for user stories. 
                                Generate a package design for the following tasks and user stories. 
                                Provide only the package design in JSON as output.

                                Generate a package design for the following user stories and tasks. 
                                The package design should outline the structure and organization of the tasks, 
                                including dependencies, timelines, and resources required. 
                                Provide only the package design as JSON as output. 

                                1. NPM, Node.js, Express, JavaScript, ejs, and CSS will later be used for the implementation.
                                2. First, consider which classes and methods you need based on the game rules.
                                3. Think about the package design, ensuring that a frontend with ejs and CSS will be created.
                                4. Format your output clearly and neatly. The names of the classes and methods, as well as the number of files and folders, are up to you.
                                5. Structure: Define the overall structure of the package, including the main components and subtasks.
                                6. Dependencies: Identify any dependencies between tasks that may affect the order of implementation.

                                Use this JSON schema. For the files (e.g class1.js, index.html) use an empty string as value:
                                
                                directories:{{
                                        "src": {{
                                                class1.js: "",
                                                ...
                                        }}
                                        "test": {{
                                                class1.test.js: "",
                                                ...
                                        }}
                                        public: {{
                                                index.html: "",
                                                style.css: "",
                                                script.js: "",
                                                ...
                                        }}
                                }}

                                Product Vision: {pVision} \n\n
                                User Storys: {userStorys} \n\n
                                Tasks: {tasks} \n\n
                                        """
    parser = JsonOutputParser(pydantic_object=List[str])
    prompt = PromptTemplate(
        template=prompt_in,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    response = generate_valid_json(chain)
    logger.info("Package design generated successfully.")
    return response.text


def generate_code(userStorys: dict, pVision: str):
    """
    Generate the following tasks based on the package design, user stories, and product vision. Each task should be implemented step by step to ensure a fully functional and valid solution. Ensure the generated code is appropriate for a project built with Node.js, Express, ejs, and CSS, and ensure all the dependencies, files, and folders are correctly structured.

    1. The implementation will be done using NPM, Node.js, Express, JavaScript, ejs, and CSS.
    2. Code for routes, controllers, models, and services should be generated in a structured and modular way.
    3. Frontend (ejs, CSS) files should be integrated correctly and align with the backend logic.
    4. Task dependencies should follow the package design with appropriate files for each module
    5. Each task should generate functional code that meets the package design, with the corresponding classes, methods, and dependencies.
    6. Ensure all tasks are properly sequenced based on dependencies, focusing on building reusable code components (models, controllers, routes).

    """


def generate_valid_json(chain: RunnableSerializable[dict, Any]) -> dict:
    """
    Generate a valid JSON output from the given chain.

    Args:
            chain (RunnableSerializable[dict, Any]): The chain to generate the JSON output from.

    Returns:
            dict: The generated JSON output

    Raises:
            ValueError: If a valid JSON output cannot be generated after multiple attempts
    """
    result = {}
    count = 0
    while count < 5:
        result = chain.invoke({})

        # Check if result is serializable to JSON
        try:
            json_str = json.dumps(result)  # Attempt to serialize
            return json.loads(
                json_str
            )  # Return deserialized dict to ensure it's valid JSON
        except (TypeError, ValueError) as e:
            logger.warning("Invalid JSON generated. Trying again...")
            logger.warning(f"Generated Output: {result}, Error: {e}")
            count += 1
    logger.error("Failed to generate valid JSON after multiple attempts.")
    raise ValueError("Failed to generate valid JSON.")


# code_filling_prompt = f"""
# Based on the following package design, implement the code for the specified classes and methods. Ensure that the code is efficient, modular, and follows best practices for JavaScript, Express, and ejs.

# Package Design: {package_design}

# Implement the following class: {class_name} with the following methods: {method_names}. Ensure that each method is fully functional and tested.
# """
