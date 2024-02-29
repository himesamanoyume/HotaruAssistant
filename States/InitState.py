from States.BaseState import BaseState
from Hotaru.Client.LogClientHotaru import logClientMgr
from Hotaru.Client.ConfigClientHotaru import configClientMgr
from Hotaru.Client.StateHotaru import stateMgr
from States.CompleteDailyState import CompleteDailyState

class InitState(BaseState):

    mStateName = 'InitState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} Begin Reload")
        configClientMgr.IsAgreeDisclaimer()
        stateMgr.Transition(CompleteDailyState())
        return True

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} Running Reload")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} Exit Reload")
