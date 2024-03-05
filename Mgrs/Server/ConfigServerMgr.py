
from Modules.Config.ConfigServerModule import ConfigServerModule
from Modules.Config.ConfigKeySubModule import ConfigKeySubModule
import sys

class ConfigServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigServerModule()
            cls.mKey = ConfigKeySubModule()

        return cls.mInstance
    
    @classmethod
    def SetConfigValue(cls, key:str, uid:str=None, value=0):
        cls.mConfig.SetConfigValue(key, uid, value)

    @classmethod
    def AppendConfigValue(cls, key:str, uid:str=None, value=0):
        cls.mConfig.AppendConfigValue(key, uid, value)

    @classmethod
    def GetConfigValue(cls, key:str, uid:str=None):
        return cls.mConfig.GetConfigValue(key, uid)
    
    @classmethod
    def DelConfigKey(cls, key:str, uid:str=None):
        return cls.mConfig.DelConfigKey(key, uid)
