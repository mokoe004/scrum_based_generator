import os
import json
from logger_config import setup_logger 

# Set up logging
logger = setup_logger("ProjectCreatorLogger", log_to_console=True)

# Function to create directories and files based on the JSON content
def create_structure(base_path, structure):
    for key, value in structure.items():
        current_path = os.path.join(base_path, key)
        
        if isinstance(value, dict):
            # If the value is a dictionary, create a directory
            logger.debug(f"Creating directory: {current_path}")
            try:
                os.makedirs(current_path, exist_ok=True)
            except OSError as e:
                logger.error(f"Error creating directory {current_path}: {e}")
            create_structure(current_path, value)
        elif isinstance(value, str):
            # If the value is a string, create a file with the specified content
            logger.debug(f"Creating file: {current_path}")
            try:
                with open(current_path, 'w') as file:
                    file.write(value)
                    logger.debug(f"Written content to file: {current_path}")
            except OSError as e:
                logger.error(f"Error creating file {current_path}: {e}")

def create(json_data):
    # Base directory where the project structure will be created
    base_directory = "generated_project"

    # Create the project structure based on the JSON data
    logger.info(f"Starting to create project structure in base directory: {base_directory}")
    try:
        create_structure(base_directory, json_data)
        logger.info("Project structure creation completed.")
    except Exception as e:
        logger.error(f"Error during project structure creation: {e}")
