from Modules.Client.GameControlModule import GameControlModule
from Modules.Utils.Retry import Retry
from Modules.Utils.Date import Date
from Hotaru.Client.LogClientHotaru import logMgr, log
from Hotaru.Client.ScreenHotaru import screenMgr

from Hotaru.Client.OcrHotaru import ocrMgr
import sys,time

class GameControlMgr:
    
    @staticmethod
    def StartGame():
        log.hr(logMgr.Hr("开始启动游戏"))
        if not Retry.Re(lambda: GameControlModule.StartGame(), 600, 1):
            log.error(logMgr.Error("启动游戏超时，退出程序"))
            input("按回车键关闭窗口. . .")
            sys.exit(1)
        
        screenMgr.mScreen.ChangeTo('menu')
        if not Retry.Re(lambda: screenMgr.mDetect.FindElement("./assets/images/menu/journey.png", "image", 0.8)):
            log.info(logMgr.Info("检测到未使用无名路途壁纸"))
            screenMgr.mScreen.ChangeTo('wallpaper')
            if Retry.Re(lambda: screenMgr.mDetect.FindElement("./assets/images/menu/wallpaper/journey.png", "image", 0.8)):
                Retry.Re(lambda: screenMgr.mDetect.ClickElement("更换", "text", max_retries=4))
            screenMgr.mDetect.pressKey("esc")
            log.info(logMgr.Info("更换到无名路途壁纸成功"))
        log.hr(logMgr.Hr("游戏启动完成"))
        
    @staticmethod
    def StopGame():
        GameControlModule.StopGame()
        ocrMgr.mOcr.ExitOcr()
        log.hr(logMgr.Hr("退出完成"), 2)

