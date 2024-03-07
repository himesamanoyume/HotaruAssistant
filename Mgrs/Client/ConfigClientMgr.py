
from Modules.Utils.ConfigKey import ConfigKey
from Modules.Config.ConfigModule import ConfigModule
from Hotaru.Client.LogClientHotaru import logMgr,log
import sys,threading,time

class ConfigClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfigModule = ConfigModule(logMgr)
            cls.mConfig = cls.mConfigModule.mConfig
            cls.mKey = ConfigKey()

        return cls.mInstance
    
    def IsAgreed2Disclaimer(self):
        if not self.mConfig[self.mKey.AGREED_TO_DISCLAIMER]:
            log.error(logMgr.Error("你未同意《免责声明》, 需要先启动Server并同意"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            self.autoSaveThread = threading.Thread(target=self.AutoSave)
            self.autoSaveThread.start()

    def AutoSave(self):
        while True:
            time.sleep(1)
            if time.time() - self.mConfigModule.mLastTimeModifyTimestamp <= 5:
                log.info(logMgr.Info("检测到配置文件修改"))
                time.sleep(5)
                if time.time() - self.mConfigModule.mLastTimeModifyTimestamp >= 5:
                    self.mConfigModule.SaveConfig()
                    log.info(logMgr.Info("配置文件已自动保存"))
    