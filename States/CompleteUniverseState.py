from States.BaseState import BaseState
from Mgrs.HotaruServerMgr import LogServerMgr,ClickMgr,ConfigMgr,JsonMgr,SocketMgr,ScreenMgr,WebMgr

class CompleteUniverseState(BaseState):

    mStateName = 'CompleteUniverseState'

    @classmethod
    def OnBegin(cls):
        LogServerMgr.Info(f"{cls.mStateName} Begin")

    @classmethod
    def OnRunning(cls):
        LogServerMgr.Info(f"{cls.mStateName} Running")

    @classmethod
    def OnExit(cls):
        LogServerMgr.Info(f"{cls.mStateName} Exit")