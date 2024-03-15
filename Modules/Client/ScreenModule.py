from Hotaru.Client.ConfigClientHotaru import configMgr
from .DetectDevScreenSubModule import DetectDevScreenSubModule
from .DetectScreenModule import DetectScreenModule
from Hotaru.Client.LogClientHotaru import logMgr,log
from Modules.Utils.GameWindow import GameWindow
import time

class ScreenModule:

    def __init__(self):
        self.mDevScreen = DetectDevScreenSubModule()
        self.mDetect = DetectScreenModule(configMgr.mKey.GAME_TITLE_NAME)
    
    def StartDevScreen(self):
        if configMgr.mConfig[configMgr.mKey.DEV_SCREEN_ENABLE]:
            log.info(logMgr.Info("DevScreen正在开启"))
            while True:
                window = GameWindow.GetWindow(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME])
                if not window is False:
                    if window.title in ["崩坏：星穹铁道"]:
                        self.mDevScreen.InitDevScreenLoop(window)
                    else:
                        log.warning(logMgr.Warning("未获取到游戏窗口,DevScreen无法开启"))
                
                print("等待窗口...")
                time.sleep(5)
        else:
            log.info(logMgr.Info("DevScreen配置未启用"))

    