
from Modules.Config.ConfigModule import ConfigModule

class ConfigMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigModule = ConfigModule()

        return cls.mInstance
    
    


        