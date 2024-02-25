
from Modules.Config.BaseConfigModule import BaseConfigModule
from Modules.Config.ConfigClientModule import ConfigClientModule

import sys

class ConfigClientMgr(BaseConfigModule):
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigClientModule = ConfigClientModule()

        return cls.mInstance
    
    @classmethod
    def SetConfig(cls):
        pass

    @classmethod
    def IsAgreeDisclaimer(cls):
        cls.mConfigClientModule.IsAgreeDisclaimer()
