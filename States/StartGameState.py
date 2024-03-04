from States import *
from Hotaru.Client.StateHotaru import stateMgr
from .LoginGameState import LoginGameState
from Hotaru.Server.ScreenHotaru import screenMgr

class StartGameState(BaseState):

    mStateName = 'StartGameState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} Begin")
        # screenMgr.DevScreen()
        logClientMgr.Screen("114,514,1919,818")
    
    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} Running")
        return stateMgr.Transition(LoginGameState())

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} Exit")
