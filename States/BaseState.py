from States.State import State
from Mgrs.HotaruClientMgr import LogClientMgr,ClickMgr,JsonMgr,SocketMgr,ScreenMgr

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
        LogClientMgr.Log(f"{cls.mStateName} BaseBegin")

    @classmethod
    def OnRunning(cls):
        LogClientMgr.Log(f"{cls.mStateName} BaseRunning")

    @classmethod
    def OnExit(cls):
        LogClientMgr.Log(f"{cls.mStateName} BaseExit")
