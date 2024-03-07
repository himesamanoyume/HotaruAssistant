from Hotaru.Client.LogClientHotaru import log, logMgr
from Hotaru.Client.ConfigClientHotaru import configMgr
import os,sys,time

class GameControlModule:

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
        
        time.sleep(10)

    @staticmethod
    def IsGameRunning():
        pass