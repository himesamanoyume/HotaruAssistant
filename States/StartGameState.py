from States import *
from Hotaru.Client.StateHotaru import stateMgr
from .LoginGameState import LoginGameState
from Hotaru.Client.ScreenHotaru import screenMgr

class StartGameState(BaseState):

    mStateName = 'StartGameState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} Begin")
        screenMgr.DevScreen()
    
    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} Running")
        return stateMgr.Transition(LoginGameState())

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} Exit")
