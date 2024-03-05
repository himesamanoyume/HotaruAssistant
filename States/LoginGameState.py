from States import *
from Hotaru.Client.StateHotaru import stateMgr

class LoginGameState(BaseState):

    mStateName = 'LoginGameState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} Begin")
        return False

    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} Running")
        return False

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} Exit")
        return False
