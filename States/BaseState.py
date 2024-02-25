from States.State import State
from Hotaru.Client.LogClientHotaru import logClientMgr

class BaseState(object):

    mStateName = 'BaseState'

    @classmethod
    def Init(cls):
        state = State(
            cls.mStateName,
            lambda:cls.OnBegin(), 
            lambda:cls.OnRunning(),
            lambda:cls.OnExit()
        )
        
        return state

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} BaseBegin")

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} BaseRunning")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} BaseExit")
