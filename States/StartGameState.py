from States import *
from Hotaru.Client.ScreenHotaru import screenMgr

class StartGameState(BaseState):

    mStateName = 'StartGameState'

    def OnBegin(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Begin"))
        # screenMgr.DevScreen()
        # logClientMgr.Screen("114,514,1919,818")
        return False
    
    def OnRunning(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Running"))
        return False

    def OnExit(self):
        return False
        # log.info(logClientMgr.Info(f"{self.mStateName} Exit"))
