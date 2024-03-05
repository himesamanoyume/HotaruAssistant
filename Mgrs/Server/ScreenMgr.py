
from Modules.Server.DevScreenModule import DevScreenModule
from Hotaru.Server.LogServerHotaru import logServerMgr
from Hotaru.Server.ConfigServerHotaru import configServerMgr
import threading

class ScreenMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance
    
    def DevScreen(self):
        pass
        # if configClientMgr.GetConfigValue(configClientMgr.mKey.DEV_SCREEN_ENABLE):
        #     if self.mScreenModule.mDevScreen.InitDevScreenLoop():
        #         logClientMgr.Info("DevScreen正在开启")
        #         self.mScreenModule.mDevScreen.StartLoop()
        #         # t = threading.Thread(target=self.mScreenModule.mDevScreen.Loop)
        #         # t.start()
        #     else:
        #         logClientMgr.Error("DevScreen启动失败")
        # else:
        #     logClientMgr.Info("DevScreen配置未开启")