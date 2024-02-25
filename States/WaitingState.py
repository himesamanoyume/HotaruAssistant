from States.BaseState import BaseState
from Mgrs.HotaruClientMgr import LogClientMgr,ClickMgr,JsonMgr,SocketMgr,ScreenMgr

class WaitingState(BaseState):

    mStateName = 'WaitingState'

    @classmethod
    def OnBegin(cls):
        LogClientMgr.Log(f"{cls.mStateName} Begin")

    @classmethod
    def OnRunning(cls):
        LogClientMgr.Log(f"{cls.mStateName} Running")

    @classmethod
    def OnExit(cls):
        LogClientMgr.Log(f"{cls.mStateName} Exit")