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
            cls.mScreen = ScreenModule()
            cls.mDetect = cls.mScreen.mDetect
            cls.mDevScreen = cls.mScreen.mDevScreen

        return cls.mInstance
    
    def GetCurrentScreen(self, autotry=True, maxRetries=5):
        self.mScreen.GetCurrentScreen(autotry, maxRetries)
        
    def CheckAndSwitch(self, title):
        return self.mScreen.CheckAndSwitch(title)

    def CheckResulotion(self, title, width, height):
        self.mScreen.CheckResulotion(title, width, height)
    
    def StartDevScreen(self):
        self.mScreen.StartDevScreen()

    def ShowDetectArea(self, detectArea):
        self.mScreen.mDevScreen.canvas.delete('all')
        Retry.Re(lambda: self.mScreen.mDevScreen.ShowDetectArea(detectArea), 1)
        self.mScreen.mDevScreen.canvas.delete('all')
