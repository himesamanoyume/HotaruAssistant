from States.BaseState import BaseState
from Mgrs.HotaruClientMgr import LogClientMgr,ClickMgr,JsonMgr,SocketMgr,ScreenMgr

class InitState(BaseState):

    mStateName = 'InitState'

    @classmethod
    def OnBegin(cls):
        LogClientMgr.Log(f"{cls.mStateName} Begin Reload")
        # WebMgr.StartServer()

    @classmethod
    def OnRunning(cls):
        LogClientMgr.Log(f"{cls.mStateName} Running Reload")

    @classmethod
    def OnExit(cls):
        LogClientMgr.Log(f"{cls.mStateName} Exit Reload")
