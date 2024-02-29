from States.BaseState import BaseState
from Hotaru.Client.LogClientHotaru import logClientMgr
from Hotaru.Client.StateHotaru import stateMgr
from States.LoginGameState import LoginGameState

class CompleteDailyState(BaseState):

    mStateName = 'CompleteDailyState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} Begin")
        stateMgr.Transition(LoginGameState())
        return True

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} Running")
        stateMgr.Transition(LoginGameState())
        return True

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} Exit")


