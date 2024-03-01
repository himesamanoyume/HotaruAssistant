from States import *
from .CompleteDailyState import CompleteDailyState

class InitState(BaseState):

    mStateName = 'InitState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} Begin Reload")
        configClientMgr.IsAgreeDisclaimer()
        return stateMgr.Transition(CompleteDailyState())

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} Running Reload")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} Exit Reload")
