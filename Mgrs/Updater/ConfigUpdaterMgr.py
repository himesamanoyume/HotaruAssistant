
from Modules.Utils.ConfigKey import ConfigKey
from Modules.Common.ConfigModule import ConfigModule

class ConfigUpdaterMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigModule()
            cls.mKey = ConfigKey()

        return cls.mInstance