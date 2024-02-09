from module.config.config import Config
import os

config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")

config.env = os.environ.copy()
config.env['PATH'] = os.path.dirname(config.python_exe_path) + ';' + config.env['PATH']
