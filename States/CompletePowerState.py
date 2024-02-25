from States.BaseState import BaseState
from Mgrs.HotaruClientMgr import LogClientMgr,ClickMgr,JsonMgr,SocketMgr,ScreenMgr

class CompletePowerState(BaseState):

    mStateName = 'CompletePowerState'

    @classmethod
    def OnBegin(cls):
        LogClientMgr.Info(f"{cls.mStateName} Begin")

    @classmethod
    def OnRunning(cls):
        LogClientMgr.Info(f"{cls.mStateName} Running")

    @classmethod
    def OnExit(cls):
        LogClientMgr.Info(f"{cls.mStateName} Exit")