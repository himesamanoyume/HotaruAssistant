from States.BaseState import BaseState
from Mgrs.HotaruClientMgr import LogClientMgr,ClickMgr,JsonMgr,SocketMgr,ScreenMgr

class IdleState(BaseState):

    mStateName = 'IdleState'

    @classmethod
    def OnBegin(cls):
        LogClientMgr.Log(f"{cls.mStateName} Begin")

    @classmethod
    def OnRunning(cls):
        LogClientMgr.Log(f"{cls.mStateName} Running")

    @classmethod
    def OnExit(cls):
        LogClientMgr.Log(f"{cls.mStateName} Exit")