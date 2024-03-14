from Hotaru.Client.LogClientHotaru import log, logMgr
from Hotaru.Client.ConfigClientHotaru import configMgr
import os,sys,time,psutil,pyautogui
from Modules.Utils.GameWindow import GameWindow
from Modules.Utils.Retry import Retry
from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.DataClientHotaru import dataMgr

class GameControlModule:

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
        if screenMgr.mDetect.ClickElement("./assets/images/screen/click_enter.png", "image", 0.9):
            return True
        screenMgr.mDetect.ClickElement("./assets/images/base/confirm.png", "image", 0.9)

        screenMgr.mDetect.ClickElement("./assets/images/base/restart.png", "image", 0.9)

        screenMgr.mDetect.ClickElement("./assets/images/base/start_game.png", "image", 0.9)
        return False
        

    @staticmethod
    def LaunchGame():
        log.info(logMgr.Info("启动游戏中..."))

        GameControlModule.CheckGamePath(configMgr.mConfig[configMgr.mKey.GAME_PATH])
        if os.system(f"cmd /C start \"\" \"{configMgr.mConfig[configMgr.mKey.GAME_PATH]}\""):
            return False
            
        time.sleep(20)
        if not Retry.Re(lambda: screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]), 180, 1):
            log.error(logMgr.Error("无法切换到游戏"))
            return False
        
        screenMgr.CheckResulotion(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME], 1920, 1080)

        if not Retry.Re(lambda: GameControlModule.CheckAndClickEnter(), 180, 1):
            log.error(logMgr.Error("无法找到点击进入按钮"))
            return False

        if not Retry.Re(lambda: screenMgr.mScreen.GetCurrentScreen(), 180, 1):
            log.error(logMgr.Error("无法进入主界面"))
            return False
        
        return True

    @staticmethod
    def StopGame():
        log.info(logMgr.Info("开始退出游戏"))
        time.sleep(1)
        if screenMgr.CheckAndSwitch(configMgr.mKey.GAME_TITLE_NAME):
            time.sleep(1)
            pyautogui.hotkey('alt','f4')
            time.sleep(5)
            if screenMgr.CheckAndSwitch(configMgr.mKey.GAME_TITLE_NAME):
                log.info(logMgr.Info("游戏退出成功"))
            else:
                pyautogui.hotkey('alt', 'f4')
                time.sleep(5)
        else:
            log.warning(logMgr.Warning("游戏已经退出了"))
        return True


    @staticmethod
    def StartGame():
        # 判断是否已经启动
        if not screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]):
            if not GameControlModule.LaunchGame():
                log.error(logMgr.Error("游戏启动失败，退出游戏进程"))
                GameControlModule.StopGame()
                return False
            else:
                log.info(logMgr.Info("游戏启动成功"))
                GameControlModule.GetGameProcessPath(configMgr.mConfig[configMgr.mKey.GAME_PROCESS_NAME])
        else:
            log.info(logMgr.Info("游戏已经启动了"))

            programPath = GameControlModule.GetGameProcessPath(configMgr.mConfig[configMgr.mKey.GAME_PROCESS_NAME])
            if programPath is not None and programPath != configMgr.mConfig[configMgr.mKey.GAME_PATH]:
                configMgr.mConfig.SetValue(configMgr.mKey.GAME_PATH, programPath)
                log.info(logMgr.Info(f"游戏路径更新成功：{programPath}"))

            screenMgr.CheckResulotion(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME], 1920, 1080)
        return True