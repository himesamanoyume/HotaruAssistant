from module.config.config import Config
from module.config.configM import ConfigM
import os

config = Config("E:/SourceCode/March7thAssistantPrivate/assets/config/version.txt","E:/SourceCode/March7thAssistantPrivate/assets/config/config.example.yaml","E:\SourceCode\March7thAssistantPrivate\config.yaml")
configM = ConfigM("./configM.example.yaml","./configM.yaml")

# config = Config("..\..\config.yaml")


def check():
    pass


check()
config.env = os.environ.copy()
config.env['PATH'] = os.path.dirname(config.python_exe_path) + ';' + config.env['PATH']
