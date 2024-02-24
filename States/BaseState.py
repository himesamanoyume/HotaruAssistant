from States.State import State
from Mgrs.HotaruServerMgr import LogServerMgr,ClickMgr,ConfigMgr,JsonMgr,SocketMgr,ScreenMgr,WebMgr

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
        LogServerMgr.Info(f"{cls.mStateName} BaseBegin")

    @classmethod
    def OnRunning(cls):
        LogServerMgr.Info(f"{cls.mStateName} BaseRunning")

    @classmethod
    def OnExit(cls):
        LogServerMgr.Info(f"{cls.mStateName} BaseExit")
