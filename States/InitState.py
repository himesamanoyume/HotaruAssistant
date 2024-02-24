from States.BaseState import BaseState
from Mgrs.HotaruServerMgr import LogServerMgr,ClickMgr,ConfigMgr,JsonMgr,SocketMgr,ScreenMgr,WebMgr

class InitState(BaseState):

    mStateName = 'InitState'

    @classmethod
    def OnBegin(cls):
        LogServerMgr.Info(f"{cls.mStateName} Begin Reload")
        ConfigMgr.IsAgreeDisclaimer()
        # WebMgr.StartServer()

    @classmethod
    def OnRunning(cls):
        LogServerMgr.Info(f"{cls.mStateName} Running Reload")

    @classmethod
    def OnExit(cls):
        LogServerMgr.Info(f"{cls.mStateName} Exit Reload")
