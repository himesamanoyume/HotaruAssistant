from States import *
from Hotaru.Client.DataClientHotaru import dataMgr
import time
from Modules.Utils.Date import Date

class WaitForNextLoopState(BaseState):

    mStateName = 'WaitForNextLoopState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        waitTime = Date.GetWaitTimeWithTotalTime(configMgr)
        futureTime = Date.CalculateFutureTime(waitTime)
        log.info(logMgr.Info(f"将在{futureTime}后继续运行"))
        # time.sleep(20)
        print(waitTime)
        time.sleep(waitTime)

    def OnExit(self):
        return False
