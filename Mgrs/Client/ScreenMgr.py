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
    
    def CheckAndSwitch(self, title):
        return self.mScreenModule.CheckAndSwitch(title)

    def CheckResulotion(self, title, width, height):
        self.mScreenModule.CheckResulotion(title, width, height)
    
    def StartDevScreen(self):
        self.mScreenModule.StartDevScreen()
