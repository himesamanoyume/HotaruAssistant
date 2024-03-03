
from Modules.Client.ScreenModule import ScreenModule
from Hotaru.Client.LogClientHotaru import logClientMgr
from Hotaru.Client.ConfigClientHotaru import configClientMgr
import threading

class ScreenMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mScreenModule = ScreenModule()

        return cls.mInstance
    
    def DevScreen(self):
        if configClientMgr.GetConfigValue(configClientMgr.mConfig.mKey.DEV_SCREEN_ENABLE):
            if self.mScreenModule.mDevScreen.InitDevScreenLoop():
                logClientMgr.Info("DevScreen正在开启")
                self.mScreenModule.mDevScreen.StartLoop()
                # t = threading.Thread(target=self.mScreenModule.mDevScreen.Loop)
                # t.start()
            else:
                logClientMgr.Error("DevScreen启动失败")
        else:
            logClientMgr.Info("DevScreen配置未开启")