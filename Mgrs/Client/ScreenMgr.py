from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.ConfigClientHotaru import configMgr
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
        # 这里也需要Server判断是否重复
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            self.window = windows[0]
            return self.window
        return False
        # end
    
    def CheckAndSwitch(self, title):
        return self.mScreenModule.CheckAndSwitch(title)

    def CheckResulotion(self, title, width, height):
        self.mScreenModule.CheckResulotion(title, width, height)
    
    def SwitchToWindow(self, title, maxRetries=5):
        self.mScreenModule.SwitchToWindow(title, maxRetries)
    
    def StartDevScreen(self):
        if configMgr.mConfig[configMgr.mKey.DEV_SCREEN_ENABLE]:
            log.info(logMgr.Info("DevScreen正在开启"))
        
            if self.GetWindow(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]).title in ["崩坏：星穹铁道"]:
                self.mScreenModule.mDevScreen.InitDevScreenLoop(self.window)
            else:
                log.warning(logMgr.Warning("未获取到游戏窗口,DevScreen无法开启"))
        else:
            log.info(logMgr.Info("DevScreen配置未启用"))
