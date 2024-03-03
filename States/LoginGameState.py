from States import *
from Hotaru.Client.StateHotaru import stateMgr
from .CompleteDailyState import CompleteDailyState

class LoginGameState(BaseState):

    mStateName = 'LoginGameState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} Begin")

    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} Running")
        return stateMgr.Transition(CompleteDailyState())

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} Exit")
