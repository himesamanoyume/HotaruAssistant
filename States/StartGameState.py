from States import *
from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.GameControlHotaru import gameMgr

class StartGameState(BaseState):

    mStateName = 'StartGameState'

    def OnBegin(self):
        log.info(logMgr.Info("开始启动游戏"))
        gameMgr.StartGame()
        return False
    
    def OnRunning(self):
        return False

    def OnExit(self):
        return False
