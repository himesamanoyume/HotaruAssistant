from ruamel.yaml import YAML
import sys,questionary
from .ConfigKeySubModule import ConfigKeySubModule

class BaseConfigModule(object):

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigKey = ConfigKeySubModule()
        return cls.mInstance
    
    def LoadConfig(self, configPath=None, exampleConfigPath = "./Assets/config/config.example.yaml"):
        self.mConfigPath = configPath
        self.mYaml = YAML()

        try:
            with open(exampleConfigPath, 'r', encoding='utf-8') as exampleConfigFile:
                exampleConfig = self.mYaml.load(exampleConfigFile)
                if exampleConfig:
                    self.mExampleConfig = exampleConfig
                print("Config文件已加载")
        except FileNotFoundError:
            print("Config文件未找到")
            sys.exit(1)
        
        configPath = self.mConfigPath if configPath is None else configPath