from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import dataMgr
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
            log.info(logMgr.Info("DevScreen正在等待开启"))
            while not dataMgr.currentAction == "临时流程":
                window = GameWindow.GetWindow(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME])
                if not window is False:
                    self.mDevScreen.InitDevScreenLoop(window)
                else:
                    self.mDevScreen.isDevScreenRunning = False
                    log.warning(logMgr.Warning("未获取到游戏窗口,DevScreen无法开启"))
                        
                log.info(logMgr.Info("等待窗口..."))
                time.sleep(5)
        else:
            log.info(logMgr.Info("DevScreen配置未启用"))

    