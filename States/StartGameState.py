from States import *
from Hotaru.Client.ScreenHotaru import screenMgr

class StartGameState(BaseState):

    mStateName = 'StartGameState'

    def OnBegin(self):
        log.info(logMgr.Info("开始启动游戏"))

        return False
    
    def OnRunning(self):
        return False

    def OnExit(self):
        return False
