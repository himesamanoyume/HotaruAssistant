
from Modules.Utils.ConfigKey import ConfigKey
# from Modules.Config.ConfigClientModule import ConfigClientModule
from Modules.Config.ConfigModule import ConfigModule
from Hotaru.Client.LogClientHotaru import logClientMgr

class ConfigClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            # cls.mConfig = ConfigClientModule()
            cls.mConfig = ConfigModule(logClientMgr)
            cls.mKey = ConfigKey()

        return cls.mInstance
    
    # @classmethod
    # def SetConfigValue(cls, key:str, uid, value=0):
    #     cls.mConfig.SetConfigValue(key, uid, value)

    # @classmethod
    # def DelConfigKey(cls, key:str, uid):
    #     cls.mConfig.DelConfigKey(key, uid)

    # @classmethod
    # def AppendConfigValue(cls, key:str, uid, value=0):
    #     cls.mConfig.AppendConfigValue(key, uid, value)

    # @classmethod
    # def GetConfigValue(cls, key:str, uid):
    #     return cls.mConfig.GetConfigValue(key, uid)
