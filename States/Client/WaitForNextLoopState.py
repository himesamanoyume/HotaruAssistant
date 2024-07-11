from States.Client import *
import time
from Modules.Utils.Date import Date

class WaitForNextLoopState(BaseClientState):

    mStateName = 'WaitForNextLoopState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        waitTime = Date.GetWaitTimeWithTotalTime(configMgr)
        futureTime = Date.CalculateFutureTime(waitTime)
        log.info(logMgr.Info(f"将在{futureTime}后继续运行"))
        time.sleep(waitTime)

    def OnExit(self):
        return False
