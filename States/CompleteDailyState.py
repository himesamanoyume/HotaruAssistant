from States import *
from Hotaru.Client.StateHotaru import stateMgr

class CompleteDailyState(BaseState):

    mStateName = 'CompleteDailyState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} Begin")

    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} Running")

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} Exit")


