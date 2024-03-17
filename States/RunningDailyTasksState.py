from States import *
import time, datetime

class RunningDailyTasksState(BaseState):

    mStateName = 'RunningDailyTasksState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    