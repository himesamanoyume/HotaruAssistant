from States.Client import *
import time
from Modules.Utils.Date import Date

class WaitForNextLoopState(BaseClientState):

    mStateName = 'WaitForNextLoopState'

    def __init__(self, _waitTime):
        super().__init__()
        self._waitTime = _waitTime

    def OnBegin(self):
        return False

    def OnRunning(self):
        waitTime = Date.GetWaitTimeWithTotalTime(self._waitTime)
        log.info(logMgr.Info(f"将在{Date.CalculateFutureTime(waitTime)}后继续运行"))
        time.sleep(waitTime)

    def OnExit(self):
        return False
