from States import *

class CompleteDailyState(BaseState):

    mStateName = 'CompleteDailyState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False


