import os, json
from typing import Any, List, Optional
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field, ValidationError

from logger_config import setup_logger

import models.user_storys as user_storys
import models.code as code

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSerializable
from langchain_core.exceptions import OutputParserException

logger = setup_logger("GeneratorLogger", "generator.log")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", api_key=os.environ.get("GOOGLE_API_KEY")
)

# model = ChatMistralAI(
#     model = "mistral-large-latest"
#     )

def generate_personas(pVision, personas_amount):
    prompt_in = f"""
                                You are a project owner, responsible for creating personas for a new project. 
                                Generate {personas_amount} personas for the following project. 
                                Provide output as specified in the format_instructions.

                                Generate {personas_amount} personas for the following project, discribed with the Product vision. 
                                Ensure that each persona is distinct, with detailed attributes based on the project vision. 
                                Each persona should be unique in terms of background, motivation, and goals. Try to cover a diverse range of potential users.
                                For each persona, consider the following attributes and context. Follow a step-by-step thought process to carefully define each aspect:\n\n

                                Product vision: {pVision}\n\n
                                
                                1. name: Choose a realistic and contextually appropriate name based on the demographics and market segment.
                                2. age: Consider the typical age range of individuals relevant to the project vision.
                                3. occupation: Identify a profession that aligns with the project's goals and the persona's motivations.
                                4. background: Detail the persona’s background, including education, experience, and personal life. Think about how this background influences their interactions with the product or service.
                                5. motivation: What drives this persona? What are their personal or professional motivations in relation to the project vision? Be specific in connecting their motivations to the project.
                                6. goal: Define the persona’s main goal when interacting with the product or service. Consider how their objectives may differ depending on their role or background.

                                Each persona should reflect a different aspect of the target audience, ensuring diversity in background, motivation, and goals. 

                                """
    response = generate_valid_json(prompt_in, user_storys.PersonaListModel)
    logger.info("Personas generated successfully.")
    return response["personas"]

def generate_epics(pVision: str, personas: dict, epics_amount: int = None):

    prompt_in = ""
    if epics_amount is not None:
        prompt_in += f"""
        You are a project owner, responsible for creating epics for a new project.
                                Generate {epics_amount} epics based on the product vision and the personas.
                                Provide output as specified in the format_instructions.

                                Generate {epics_amount} epics based on the following product vision and personas.
                                """
    else:
        prompt_in += f"""
                                You are a project owner, responsible for creating epics for a new project.
                                Generate epics based on the product vision and the personas.
                                Provide output as specified in the format_instructions.

                                Generate epics based on the following product vision and personas.
                                """
    prompt_in += f"""
                                Ensure that each epic contains a clear business value that aligns with the overall product vision.
                                For each epic, consider the following attributes and context. Follow a step-by-step thought process to carefully define each aspect:

                                1. name: Choose a descriptive name that reflects the core theme or goal of the epic.
                                2. description: Provide a brief description of the epic, outlining the main features or functionality it encompasses.
                                3. business_value: Define the business value or impact of the epic in relation to the product vision. Consider how this epic contributes to the overall success of the project.

                                Each epic should represent a significant feature or functionality within the project, with a clear business value and impact on the product vision.

                                Product Vision: {pVision} \n\n
                                Personas: {personas} \n\n
                                """
    response = generate_valid_json(prompt_in, user_storys.EpicListModel)
    logger.info("Epics generated successfully.")
    logger.info(response)
    return response["epics"]


def generate_user_storys(pVision: str, personas: dict, epic: dict):
    prompt_in = f"""
                                You are a project owner, responsible for creating user_stories for a new project. 
                                Generate user_storys for the given epic, based on the product vision and the personas.
                                Always use one persona as the subject of the user_story. 
                                Provide output as specified in the format_instructions.

                                Generate user_stories based on the following personas and product vision. Ensure that each epic contains a clear business value and that user_stories follow the format: "As a [persona], I want to [goal], so that [benefit]." 

                                Important Guidelines:
                                1. persona Selection: The actor for each user_story must be one of the predefined personas listed below.
                                2. business_value: Each epic must have a clear business_value that aligns with the overall product vision.
                                3. No acceptance_criteria: Do not include acceptance criteria for either epics or user_stories.
                                4. Realistic Goals: The goals in the user_stories must be achievable and grounded, as they will serve as the basis for small-scale code generation.
                                5. Output Format: Return the result in valid JSON format, with epics and their corresponding user_stories.
                                6. acceptance_criteria:  Generate between 3 and 8 acceptance criteria. Ensure that the acceptance criteria are specific, measurable, and achievable. 
                                    6.1 Clarity: Each acceptance criterion is specific and easy to understand.
                                    6.2 Measurability: The criteria must be testable and verifiable, either through automated tests or manual review.
                                    6.3 Focus on the outcome: The criteria should describe what the system needs to do, not how to do it.
                                    6.4 Edge Cases: Consider edge cases and sure that each negative scenarios where the system might fail or need to handle errors gracefully.
                                    6.5 User Perspective: Write the acceptance criteria from the personas perspective of the user story, focusing on their interactions and expectations.
                                    6.6 Success Conditions: Define what constitutes success for each user story, including any conditions for completing the feature.
                                
                                Personas: {personas.__str__} \n\n
                                Product Vision: {pVision} \n\n
                                Epic: {epic} \n\n
                """
    response = generate_valid_json(prompt_in, user_storys.UserStoryListModel)
    logger.info("User stories generated successfully.")
    logger.info(response)
    return response["user_stories"]

def generate_tasks(userStories: dict):
    prompt_in = f"""
                                You are a project owner, responsible for creating tasks for user stories. 
                                Generate tasks for the following user stories. 
                                Provide output as specified in the format_instructions.

                                Ensure that the tasks are specific, actionable, and focused on the implementation details. 
                                For the following User Stories provided in JSON format, generate tasks. 
                                The tasks should be clear, actionable, and focused on the steps needed to implement the user story. 
                                Follow these best practices when creating the tasks:

                                Best Practices:
                                1. Specificity: Each task should be specific and focused on a single action or goal.
                                2. Actionable: The tasks should be actionable and clearly defined, with a clear outcome or result.
                                3. Implementation Details: Focus on the steps needed to implement the user story, rather than high-level goals.
                                4. Dependencies: Consider any dependencies or prerequisites for each task, including external services or resources.
                                5. Testability: Ensure that each task can be tested and verified, either through automated tests or manual review.
                                6. Priority: Assign a priority or order to the tasks based on their importance and impact on the user story.

                                User Story: {userStories} \n\n
                                        """
    
    response = generate_valid_json(prompt_in, user_storys.TasksModel)
    logger.info("Tasks generated successfully.")
    return response["tasks"]

def generate_package_design(tasks: dict, userStorys: dict, pVision: str):
    prompt_in = f"""
                                You are a project owner, responsible for creating a package design for user stories. 
                                Generate only the package design for the following tasks and user stories. 
                                Provide output as specified in the format_instructions.

                                The package design should outline the structure and organization of the tasks, 
                                including dependencies, timelines, and resources required. 

                                1. NPM, Node.js, Express, JavaScript, ejs, CSS and SQLite will later be used for the implementation.
                                2. First, consider which classes and methods you need based.
                                3. Think about the package design, ensuring that a frontend with ejs and CSS will be created.
                                4. Format your output clearly and neatly. The names of the classes and methods, as well as the number of files and folders, are up to you.
                                5. Structure: Define the overall structure of the package, including the main components and subtasks.
                                6. Dependencies: Identify any dependencies between tasks that may affect the order of implementation.

                                Use for the format_instructions for the Output an keep in mind:
                                    When you want to display a directory use the name as key and a dict with the files or other directorys as value. 
                                    When you want to display a file use the name including suffix as key and a empty string as value.

                                Product Vision: {pVision} \n\n
                                User Storys: {userStorys} \n\n
                                Tasks: {tasks} \n\n
                                        """
    response = generate_valid_json(prompt_in, code.PackageModel)
    logger.info("Package design generated successfully.")
    return response


def generate_code(tasks: dict, pVision: str, package_design: dict):
    prompt_in = f"""
    Generate the following classes and files based on the package design, tasks, and product vision. Each task should be implemented step by step to ensure a fully functional and valid solution. 
    Ensure the generated code is appropriate for a project built with Node.js, Express, ejs, and CSS, and ensure all the dependencies, files, and folders are correctly structured.
    Every file should be filled with code that aligns with the task requirements and the overall package design.

    1. The implementation will be done using NPM, Node.js, Express, JavaScript, ejs, CSS and SQLite.
    2. Code for routes, controllers, models, and services should be generated in a structured and modular way.
    3. Frontend (ejs, CSS) files should be integrated correctly and align with the backend logic.
    4. Task dependencies should follow the package design with appropriate files for each module
    5. Each task should generate functional code that meets the package design, with the corresponding classes, methods, and dependencies.
    6. Ensure all tasks are properly sequenced based on dependencies, focusing on building reusable code components (models, controllers, routes).

    Product Vision: {pVision} \n\n
    Tasks: {tasks} \n\n
    Package Design: {package_design} \n\n
    """
    response = generate_valid_json(prompt_in, code.PackageModel)
    logger.info("Code generated successfully.")
    return response

def generate_tests(tasks: dict, pVision: str, generated_code: dict):
    prompt_in = f"""
    Generate the following tests based on the code, tasks, and product vision. Each test should validate the functionality and integrity of the code generated for the project. 
    Ensure that the tests cover all critical components of the project, including routes, controllers, models, and services. 
    The tests should be structured and modular, following best practices for unit and integration testing in Node.js.

    1. The tests will be implemented using NPM, Node.js, Express, JavaScript, ejs, CSS and SQLite.
    2. Test each module (routes, controllers, models, services) individually to ensure they function correctly.
    3. Include both unit tests and integration tests to validate the interactions between components.
    4. Ensure the tests cover all critical functionality and edge cases to validate the robustness of the code.
    5. Each test should be clearly defined, with specific test cases and expected outcomes.
    6. Follow best practices for testing in Node.js, including mocking, assertions, and test coverage.

    Product Vision: {pVision} \n\n
    Tasks: {tasks} \n\n
    Code: {generated_code} \n\n
    """
    response = generate_valid_json(prompt_in, code.TestsModel)
    logger.info("Tests generated successfully.")
    return response


def generate_valid_json(prompt_in: str, scheme: BaseModel) -> dict:
    """
    Generate valid JSON output based on the given prompt and Pydantic scheme.

    Args:
        prompt_in (str): The prompt to generate the JSON output.
        scheme (BaseModel): The Pydantic scheme to validate the generated JSON.

    Returns:
        dict: The generated JSON output that is valid based on the scheme.

    Raises:
        ValueError: If the generated JSON is invalid after multiple attempts

    """
    result = {}
    count = 0

    parser = JsonOutputParser(pydantic_object=scheme)
    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser

    while count < 5:
        # Check if result is serializable to JSON
        try:
            result = chain.invoke({"query": prompt_in})
            scheme.model_validate(result)
            # result = scheme(**result)
            return result
        except (TypeError, ValueError, OutputParserException, ValidationError) as e:
            logger.warning("Invalid JSON generated. Trying again...")
            logger.warning(f"Generated Output: {result},\n Error: {e}")
            count += 1
    logger.error("Failed to generate valid JSON after multiple attempts.")
    raise ValueError("Failed to generate valid JSON.")