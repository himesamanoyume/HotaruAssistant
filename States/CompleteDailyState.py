from States import *
from .LoginGameState import LoginGameState

class CompleteDailyState(BaseState):

    mStateName = 'CompleteDailyState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} Begin")
        return stateMgr.Transition(LoginGameState())

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} Running")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} Exit")


