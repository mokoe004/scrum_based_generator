# logger_config.py
import logging
import os

def setup_logger(name, file_name: str = None, log_to_console: bool = True, level=logging.INFO):
    """
    Setup a logger with the given name and optional file and console logging.

    Parameters:
    - name: The name of the logger.
    - file_name: The name of the file to log to (if required).
    - log_to_console: Boolean, if True logs to console.
    - log_to_file: Boolean, if True logs to a file.
    - level: The log level for the logger.

    Returns:
    - logger: The logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set the log level for the logger
    
    # Remove existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler (for logging to a file)
    if file_name:
        # Create directory if it doesn't exist
        os.makedirs('loggs', exist_ok=True)
        file_path = os.path.join('loggs', file_name)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Console handler (for logging to the console)
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Set the log level for the console handler
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
