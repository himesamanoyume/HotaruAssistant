
from Modules.Config.BaseConfigModule import BaseConfigModule
from Modules.Config.ConfigServerModule import ConfigServerModule

import sys

class ConfigServerMgr(BaseConfigModule):
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigServerModule = ConfigServerModule()

        return cls.mInstance
    
    @classmethod
    def SetConfig(cls):
        pass

    @classmethod
    def IsAgreeDisclaimer(cls):
        cls.mConfigServerModule.IsAgreeDisclaimer()
