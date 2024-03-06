
from Modules.Utils.ConfigKey import ConfigKey
from Modules.Config.ConfigModule import ConfigModule
from Hotaru.Client.LogClientHotaru import logClientMgr,log
import sys

class ConfigClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigModule = ConfigModule(logClientMgr)
            cls.mConfig = cls.mConfigModule.mConfig
            cls.mKey = ConfigKey()

        return cls.mInstance
    
    def IsAgreed2Disclaimer(self):
        if not self.mConfig[self.mKey.AGREED_TO_DISCLAIMER]:
            log.error(logClientMgr.Error("你未同意《免责声明》, 需要先启动Server并同意"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    