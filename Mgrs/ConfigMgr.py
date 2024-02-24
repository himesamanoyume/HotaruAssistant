
from Modules.Config.ConfigModule import ConfigModule
from Mgrs.HotaruServerMgr import LogServerMgr
import sys

class ConfigMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigModule = ConfigModule()

        return cls.mInstance
    
    @classmethod
    def SetConfig(cls):
        pass

    @classmethod
    def IsAgreeDisclaimer(cls):
        cls.mConfigModule.IsAgreeDisclaimer()
