from States import *
from Hotaru.Client.DataClientHotaru import dataMgr
from Hotaru.Client.ScreenHotaru import screenMgr
from Modules.Utils.Retry import Retry
import os,sys,time,psutil

class StartGameState(BaseState):

    mStateName = 'StartGameState'

    def OnBegin(self):
        log.hr(logMgr.Hr("开始启动游戏"))
        if not Retry.Re(lambda: StartGameState.IsGameRunning(), 600, 1):
            log.error(logMgr.Error("启动游戏超时，退出程序"))
            return False
            input("按回车键关闭窗口. . .")
            sys.exit(1)
        
        screenMgr.ChangeTo('menu')

        if not Retry.Re(lambda: screenMgr.FindElement("./assets/images/menu/journey.png", "image", 0.8)):
            log.info(logMgr.Info("检测到未使用无名路途壁纸"))
            Retry.Re(lambda: screenMgr.ChangeTo('wallpaper'))
            if Retry.Re(lambda: screenMgr.ClickElement("./assets/images/menu/wallpaper/journey.png", "image", 0.8)):
                Retry.Re(lambda: screenMgr.ClickElement("更换", "text", max_retries=4))
                screenMgr.PressKey("esc")
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
    
    @staticmethod
    def IsGameRunning():
        log.info(logMgr.Info("判断是否已经启动"))
        if not screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]):
            if not StartGameState.LaunchGame():
                log.error(logMgr.Error("游戏启动失败，退出游戏进程"))
                # GameControlModule.StopGame()
                return True
            else:
                log.info(logMgr.Info("游戏启动成功"))
                StartGameState.GetGameProcessPath(configMgr.mConfig[configMgr.mKey.GAME_PROCESS_NAME])
        else:
            log.info(logMgr.Info("游戏已经启动了"))

            programPath = StartGameState.GetGameProcessPath(configMgr.mConfig[configMgr.mKey.GAME_PROCESS_NAME])
            if programPath is not None and programPath != configMgr.mConfig[configMgr.mKey.GAME_PATH]:
                configMgr.mConfig.SetValue(configMgr.mKey.GAME_PATH, programPath)
                log.info(logMgr.Info(f"游戏路径更新成功：{programPath}"))

            screenMgr.CheckResulotion(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME], 1920, 1080)
        return True
    
    @staticmethod
    def LaunchGame():
        log.info(logMgr.Info("启动游戏中..."))

        StartGameState.CheckGamePath(configMgr.mConfig[configMgr.mKey.GAME_PATH])
        if os.system(f"cmd /C start \"\" \"{configMgr.mConfig[configMgr.mKey.GAME_PATH]}\""):
            return False
            
        time.sleep(20)
        if not Retry.Re(lambda: screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]), 180, 1):
            log.error(logMgr.Error("无法切换到游戏"))
            return False
        
        screenMgr.CheckResulotion(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME], 1920, 1080)

        if not Retry.Re(lambda: StartGameState.CheckAndClickEnter(), 60, 2):
            log.error(logMgr.Error("无法找到点击进入按钮"))
            return False

        if not Retry.Re(lambda: screenMgr.GetCurrentScreen(), 180, 1):
            log.error(logMgr.Error("无法进入主界面"))
            return False
        
        return True
    
    @staticmethod
    def GetGameProcessPath(name):
        # 通过进程名获取运行路径
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if name in proc.info['name']:
                dataMgr.currentGamePid = proc.info['pid']
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
        
        if screenMgr.FindElement("./assets/images/screen/click_enter.png", "image", 0.9):
            return screenMgr.ClickElement("./assets/images/screen/click_enter.png", "image", 0.9)
        else:
            if screenMgr.FindElement("./assets/images/base/confirm.png", "image", 0.9):
                screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9)
            if screenMgr.FindElement("./assets/images/base/restart.png", "image", 0.9):
                screenMgr.ClickElement("./assets/images/base/restart.png", "image", 0.9)
            if screenMgr.FindElement("./assets/images/screen/start_game.png", "image", 0.9):
                screenMgr.ClickElement("./assets/images/screen/start_game.png", "image", 0.9)
        return False
