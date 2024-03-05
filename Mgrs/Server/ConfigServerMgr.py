
# from Modules.Config.ConfigServerModule import ConfigServerModule
from Modules.Utils.ConfigKey import ConfigKey
from Modules.Config.ConfigModule import ConfigModule
from Hotaru.Server.LogServerHotaru import logServerMgr
import sys

class ConfigServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigModule = ConfigModule(logServerMgr)
            cls.mConfig = cls.mConfigModule.mConfig
            # cls.mConfig = ConfigModule(logServerMgr)
            cls.mKey = ConfigKey()

        return cls.mInstance
    
