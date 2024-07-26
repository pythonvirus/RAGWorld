import logging
import os
from Constants import TIMESTAMP


LOG_FILE = f"{TIMESTAMP}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


class CustomLogger:

    def __init__(self, name):
        self.logger = logging.getLogger(name) #By using a logger with a name, you can easily filter and analyze log messages based on their source
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(LOG_FILE_PATH,encoding='utf-8')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
    
    def inspect(self,state):
        """Print the state passed between Runnables in a langchain and pass it on"""
        self.info(state)
        return state

