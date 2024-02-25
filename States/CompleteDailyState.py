from States.BaseState import BaseState
from Hotaru.Client.LogClientHotaru import logClientMgr

class CompleteDailyState(BaseState):

    mStateName = 'CompleteDailyState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} Begin")

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} Running")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} Exit")


