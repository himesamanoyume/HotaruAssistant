from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.ConfigClientHotaru import configMgr
from Modules.Client.ScreenModule import ScreenModule
from Modules.Utils.Retry import Retry
import pyautogui

class ScreenMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mScreenModule = ScreenModule()

        return cls.mInstance
    
    def GetCurrentScreen(self, autotry=True, maxRetries=5):
        self.mScreenModule.GetCurrentScreen(autotry, maxRetries)
        
    def CheckAndSwitch(self, title):
        return self.mScreenModule.CheckAndSwitch(title)

    def CheckResulotion(self, title, width, height):
        self.mScreenModule.CheckResulotion(title, width, height)
    
    def StartDevScreen(self):
        self.mScreenModule.StartDevScreen()

    def ShowDetectArea(self, detectArea):
        self.mScreenModule.mDevScreen.canvas.delete('all')
        Retry.RepeatAttempt(lambda: self.mScreenModule.mDevScreen.ShowDetectArea(detectArea), 1)
        self.mScreenModule.mDevScreen.canvas.delete('all')
