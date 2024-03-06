from Hotaru.Client.LogClientHotaru import logClientMgr,log
from Hotaru.Client.ConfigClientHotaru import configClientMgr
from Modules.Client.ScreenModule import ScreenModule
import pyautogui

class ScreenMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mScreenModule = ScreenModule()

        return cls.mInstance
    
    def GetWindow(self, title):
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            self.window = windows[0]
            return self.window
        return False
    
    def StartDevScreen(self):
        if configClientMgr.mConfig[configClientMgr.mKey.DEV_SCREEN_ENABLE]:
            log.info(logClientMgr.Info("DevScreen正在开启"))
            if self.window in "崩坏：星穹铁道":
                self.mScreenModule.mDevScreen.InitDevScreenLoop()
            else:
                log.warning(logClientMgr.Warning("未获取到游戏窗口,DevScreen无法开启"))
        else:
            log.info(logClientMgr.Info("DevScreen配置未启用"))
