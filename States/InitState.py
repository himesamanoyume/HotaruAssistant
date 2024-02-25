from States.BaseState import BaseState
from Hotaru.Client.LogClientHotaru import logClientMgr

class InitState(BaseState):

    mStateName = 'InitState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} Begin Reload")
        # WebMgr.StartServer()

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} Running Reload")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} Exit Reload")
