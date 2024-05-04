from States.Client import *
from Modules.Utils.Retry import Retry
import os,sys,time,psutil

class ClientStartGameState(BaseClientState):

    mStateName = 'ClientStartGameState'

    def OnBegin(self):
        log.hr(logMgr.Hr("开始启动游戏"))
        if not Retry.Re(lambda: self.IsGameRunning(), 600, 1):
            log.error(logMgr.Error("启动游戏超时，退出程序"))
            return True
        
        screenClientMgr.ChangeTo('menu')

        if not Retry.Re(lambda: screenClientMgr.FindElement("./assets/static/images/menu/journey.png", "image", 0.8)):
            log.info(logMgr.Info("检测到未使用无名路途壁纸"))
            Retry.Re(lambda: screenClientMgr.ChangeTo('wallpaper'))
            if Retry.Re(lambda: screenClientMgr.ClickElement("./assets/static/images/menu/wallpaper/journey.png", "image", 0.8)):
                Retry.Re(lambda: screenClientMgr.ClickElement("更换", "text", maxRetries=4))
                screenClientMgr.PressKey("esc")
                log.info(logMgr.Info("更换到无名路途壁纸成功"))
            else:
                return False
        else:
            log.hr(logMgr.Hr("游戏启动完成"))
            return True
    
    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    def IsGameRunning(self):
        log.info(logMgr.Info("判断是否已经启动"))
        if not screenClientMgr.CheckAndSwitch(dataClientMgr.gameTitleName):
            if not self.LaunchGame():
                log.error(logMgr.Error("游戏启动失败，退出游戏进程"))
                # GameControlModule.StopGame()
                return True
            else:
                log.info(logMgr.Info("游戏启动成功"))
                self.GetGameProcessPath(configMgr.mConfig[configMgr.mKey.GAME_PROCESS_NAME])
        else:
            log.info(logMgr.Info("游戏已经启动了"))

            programPath = self.GetGameProcessPath(configMgr.mConfig[configMgr.mKey.GAME_PROCESS_NAME])
            if programPath is not None and programPath != configMgr.mConfig[configMgr.mKey.GAME_PATH]:
                configMgr.mConfig.SetValue(configMgr.mKey.GAME_PATH, programPath)
                log.info(logMgr.Info(f"游戏路径更新成功：{programPath}"))

            screenClientMgr.CheckResulotion(dataClientMgr.gameTitleName, 1920, 1080)
        return True
    
    def LaunchGame(self):
        log.info(logMgr.Info("启动游戏中..."))

        self.CheckGamePath(configMgr.mConfig[configMgr.mKey.GAME_PATH])
        if os.system(f"cmd /C start \"\" \"{configMgr.mConfig[configMgr.mKey.GAME_PATH]}\""):
            return False
            
        time.sleep(20)
        if not Retry.Re(lambda: screenClientMgr.CheckAndSwitch(dataClientMgr.gameTitleName), 180, 1):
            log.error(logMgr.Error("无法切换到游戏"))
            return False
        
        screenClientMgr.CheckResulotion(dataClientMgr.gameTitleName, 1920, 1080)

        if not Retry.Re(lambda: self.CheckAndClickEnter(), 180, 2):
            log.error(logMgr.Error("无法找到点击进入按钮"))
            return False
        
        time.sleep(5)

        if not Retry.Re(lambda: screenClientMgr.GetCurrentScreen(), 180, 1):
            log.error(logMgr.Error("无法进入主界面"))
            return False
        
        return True
    
    @staticmethod
    def GetGameProcessPath(name):
        # 通过进程名获取运行路径
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if name in proc.info['name']:
                dataClientMgr.currentGamePid = proc.info['pid']
                process = psutil.Process(proc.info['pid'])
                return process.exe()
        return None

    @staticmethod
    def CheckGamePath(path):
        # 检测路径是否存在
        if not os.path.exists(path):
            log.error(logMgr.Error(f"游戏路径不存在: {path}"))
            log.info(logMgr.Info("第一次使用请手动启动游戏进入主界面后重新运行，程序会自动保存游戏路径"))
            log.info(logMgr.Info("注意:程序只支持PC端运行,不支持任何模拟器"))
            input("按回车键关闭窗口. . .")
            sys.exit(1)

    @staticmethod
    def CheckAndClickEnter():
        if screenClientMgr.FindElement("./assets/static/images/screen/click_enter.png", "image", 0.9):
            return screenClientMgr.ClickElement("./assets/static/images/screen/click_enter.png", "image", 0.9)
        else:
            if screenClientMgr.FindElement("./assets/static/images/base/confirm.png", "image", 0.9):
                screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9)
            if screenClientMgr.FindElement("./assets/static/images/base/restart.png", "image", 0.9):
                screenClientMgr.ClickElement("./assets/static/images/base/restart.png", "image", 0.9)
            if screenClientMgr.FindElement("./assets/static/images/screen/start_game.png", "image", 0.9):
                screenClientMgr.ClickElement("./assets/static/images/screen/start_game.png", "image", 0.9)
            if screenClientMgr.FindElement("./assets/static/images/login/protocol.png", "image", 0.9):
                screenClientMgr.ClickElement("./assets/static/images/login/protocol_agree.png", "image", 0.9)
        return False
