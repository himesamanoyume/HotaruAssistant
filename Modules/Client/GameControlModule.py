from Hotaru.Client.LogClientHotaru import log, logMgr
from Hotaru.Client.ConfigClientHotaru import configMgr
import os,sys,time,psutil
from Hotaru.Client.AutoHotaru import autoMgr
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
    def LaunchGame():
        log.info(logMgr.Info("启动游戏中..."))

        GameControlModule.CheckGamePath(configMgr.mConfig[configMgr.mKey.GAME_PATH])
        if os.system(f"cmd /C start \"\" \"{configMgr.mConfig[configMgr.mKey.GAME_PATH]}\""):
            return False
            
        time.sleep(20)
        if not autoMgr.RepeatAttempt(lambda: screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]), 180, 1):
            log.error(logMgr.Error("无法切换到游戏"))
            return False
        
        screenMgr.CheckResulotion(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME], 1920, 1080)

        return True

    @staticmethod
    def StopGame():
        pass

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