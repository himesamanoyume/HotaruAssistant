
from ruamel.yaml import YAML
import sys,questionary
from .ConfigKeySubModule import ConfigKeySubModule
from Hotaru.Client.LogClientHotaru import logClientMgr
from Modules.Config.BaseConfigModule import BaseConfigModule

class ConfigClientModule(BaseConfigModule):

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            logClientMgr.Info("Config文件已加载")
        return cls.mInstance
    
    def ReadConfigByUid(self, uid):
        pass

    @classmethod
    def IsAgreeDisclaimer(cls):
        #  if not  xx[cls.mConfigKey.agreed_to_disclaimer]:
        if True:
            logClientMgr.Error("你未同意《免责声明》")
