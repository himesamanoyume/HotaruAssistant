from States import *
from Hotaru.Client.OcrClientHotaru import ocrClientMgr
from Hotaru.Client.StateHotaru import stateMgr

class InitState(BaseState):

    mStateName = 'InitState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} Begin Reload")
        configClientMgr.mConfig.IsAgreeDisclaimer()
        ocrClientMgr.CheckPath()
        return False

    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} Running Reload")
        return False

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} Exit Reload")
        return False
