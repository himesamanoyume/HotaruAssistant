from datetime import datetime
import logging
import os
import glob

from .coloredformatter import ColoredFormatter
from .titleformatter import TitleFormatter


class Logger:
    _instance = None

    def __new__(cls, level="INFO"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._create_logger(level)
        return cls._instance

    def current_datetime(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def clear_log(self, directory):
        files = glob.glob(directory + '/*')
        for f in files:
            if os.path.isfile(f):
                if os.path.getsize(f) <= 2048:
                    os.remove(f)
                

    def _create_logger(self, level="INFO"):
        self.logger = logging.getLogger('HotaruAssistant')
        self.logger.propagate = False
        self.logger.setLevel(level)

        if not os.path.exists("logs"):
            os.makedirs("logs")

        self.clear_log("./logs")
        
        file_handler = logging.FileHandler(f"./logs/{self.current_datetime()}.log", encoding="utf-8")
        file_formatter = logging.Formatter('├ %(levelname)s|%(asctime)s|%(filename)s:%(lineno)d\n└ %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter('├ %(levelname)s|%(asctime)s|%(filename)s:%(lineno)d\n└ %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.hr = TitleFormatter.format_title

        return self.logger

    def get_logger(self):
        return self.logger
