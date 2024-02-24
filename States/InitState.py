from Mgrs.HotaruMgr import LogMgr
from States.State import State

class InitState:

    mStateName = 'InitState'

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
        LogMgr.Info(f"{cls.mStateName} Begin")

    @classmethod
    def OnRunning(cls):
        LogMgr.Info(f"{cls.mStateName} Running")

    @classmethod
    def OnExit(cls):
        LogMgr.Info(f"{cls.mStateName} Exit")
