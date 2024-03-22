
from Modules.Utils.ConfigKey import ConfigKey
from Modules.Config.ConfigModule import ConfigModule
from Hotaru.Client.LogClientHotaru import logMgr,log
import sys,threading,time

class ConfigClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigModule(logMgr)
            cls.mKey = ConfigKey()

        return cls.mInstance
    
    def SaveTimestampByUid(self, key, uid):
        if key == {}:
            self.mConfig[key][uid] = 0
            self.mConfig[key][uid] = time.time()
        else:
            self.mConfig[key][uid] = time.time()
        
        return True
    
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
            time.sleep(4)
            nowtime = time.time()
            if nowtime - self.mConfig.mLastTimeSaveTimestamp >= 5 and nowtime - self.mConfig.mLastTimeModifyTimestamp <= 5:
                self.mConfig.SaveConfig()
                logMgr.Info("Client:配置文件进行自动保存")