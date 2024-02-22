
from ruamel.yaml import YAML
import sys
from .ConfigKeySubModule import ConfigKeySubModule
from Mgrs.HotaruMgr import LogMgr

class ConfigModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mInstance.LoadConfig()
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
        except FileNotFoundError:
            LogMgr.Info("Config文件未找到")
            sys.exit(1)
        
        configPath = self.mConfigPath if configPath is None else configPath
    
    def ReadConfigByUid(self, uid):
        pass
