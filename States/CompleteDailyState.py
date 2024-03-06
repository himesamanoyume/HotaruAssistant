from States import *

class CompleteDailyState(BaseState):

    mStateName = 'CompleteDailyState'

    def OnBegin(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Begin"))
        return False

    def OnRunning(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Running"))
        return False

    def OnExit(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Exit"))
        return False


