from States import *
from .CompleteDailyState import CompleteDailyState
from Hotaru.Client.OcrClientHotaru import ocrClientMgr
from Hotaru.Client.StateHotaru import stateMgr

class InitState(BaseState):

    mStateName = 'InitState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} Begin Reload")
        configClientMgr.mConfig.IsAgreeDisclaimer()
        ocrClientMgr.CheckPath()
        return stateMgr.Transition(CompleteDailyState())

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} Running Reload")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} Exit Reload")
