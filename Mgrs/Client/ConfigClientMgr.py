

from Modules.Config.ConfigClientModule import ConfigClientModule

class ConfigClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigClientModule()

        return cls.mInstance
    
    @classmethod
    def SetConfigValue(cls, key:str, uid:str=None, value=0):
        cls.mConfig.SetConfigValue(key, uid, value)

    @classmethod
    def GetConfigValue(cls, key:str, uid:str=None):
        # return cls.__mConfig.GetConfigValue(key, uid)
        cls.mConfig.GetConfigValue(key, uid)
