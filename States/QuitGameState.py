from States import *
from Hotaru.Client.DataClientHotaru import dataMgr
from Hotaru.Client.OcrHotaru import ocrMgr
from Hotaru.Client.ScreenHotaru import screenMgr
import os,sys,time,psutil,pyautogui

class QuitGameState(BaseState):

    mStateName = 'QuitGameState'

    def OnBegin(self):
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

        ocrMgr.mOcr.ExitOcr()
        log.hr(logMgr.Hr("退出完成"), 2)
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        dataMgr.ResetData()
        return False
