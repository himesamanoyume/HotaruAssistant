
from Modules.Config.ConfigKeySubModule import ConfigKeySubModule
from Modules.Config.ConfigClientModule import ConfigClientModule

class ConfigClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigClientModule()
            cls.mKey = ConfigKeySubModule()

        return cls.mInstance
    
    @classmethod
    def SetConfigValue(cls, key:str, uid, value=0):
        cls.mConfig.SetConfigValue(key, uid, value)

    @classmethod
    def DelConfigKey(cls, key:str, uid, value=0):
        cls.mConfig.DelConfigKey(key, uid, value)

    @classmethod
    def AppendConfigValue(cls, key:str, uid, value=0):
        cls.mConfig.AppendConfigValue(key, uid, value)

    @classmethod
    def GetConfigValue(cls, key:str, uid):
        # return cls.__mConfig.GetConfigValue(key, uid)
        return cls.mConfig.GetConfigValue(key, uid)
