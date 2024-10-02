# logger_config.py
import logging
import os

def setup_logger(name, file_name: str = None, level=logging.INFO):
    """
    Setup a logger with the given name and an optional file name and log level.

    Parameters:
    - name: The name of the logger.
    - file_name: The name of the file to log to (if required).
    - level: The log level for the logger.

    Returns:
    - logger: The logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Setze das Log-Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    # Zweiter Logger, der in eine Datei loggt GEHT NICHT
    if(file_name):
                # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs('loggs', exist_ok=True)
        file_path = os.path.join('loggs', file_name)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Erstelle einen Konsolen-Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # Setze das Log-Level für den Handler

    # Erstelle ein Format für die Log-Nachrichten
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Füge den Handler dem Logger hinzu
    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger

