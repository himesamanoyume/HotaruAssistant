
from Modules.Config.ConfigServerModule import ConfigServerModule

import sys

class ConfigServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigServerModule()

        return cls.mInstance
    
    @classmethod
    def SetConfigValue(cls, key:str, uid:str=None, value=0):
        cls.mConfig.SetConfigValue(key, uid, value)

    @classmethod
    def GetConfigValue(cls, key:str, uid:str=None):
        return cls.mConfig.GetConfigValue(key, uid)
            
    @classmethod
    def IsAgreeDisclaimer(cls):
        cls.mConfig.IsAgreeDisclaimer()
