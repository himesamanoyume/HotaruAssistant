from States import *
from Hotaru.Client.DataClientHotaru import dataMgr
from Hotaru.Client.OcrHotaru import ocrMgr
from Hotaru.Client.ScreenHotaru import screenMgr
import os,sys,time,psutil,pyautogui
from Modules.Utils.Retry import Retry

class QuitGameState(BaseState):

    mStateName = 'QuitGameState'

    def OnBegin(self):
        log.info(logMgr.Info("开始退出游戏"))
        time.sleep(1)
        if screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]):
            time.sleep(1)
            if not QuitGameState.TerminateProcess(configMgr.mConfig[configMgr.mKey.GAME_PROCESS_NAME]):
                time.sleep(5)
                if screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]):
                    log.info(logMgr.Info("游戏退出成功"))
                else:
                    pyautogui.hotkey('alt', 'f4')
                    time.sleep(5)
                log.error(logMgr.Error("游戏退出失败"))
                return False  
        else:
            log.warning(logMgr.Warning("游戏已经退出了"))

        ocrMgr.mOcr.ExitOcr()
        log.hr(logMgr.Hr("退出完成"), 2)

    def OnRunning(self):
        return False

    def OnExit(self):
        dataMgr.ResetData()
        return False
    
    @staticmethod
    def TerminateProcess(name, timeout=10):
        # 根据进程名中止进程
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if name in proc.info['name']:
                try:
                    process = psutil.Process(proc.info['pid'])
                    process.terminate()
                    process.wait(timeout)
                    return True
                except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied):
                    pass
        return False
