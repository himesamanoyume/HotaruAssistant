from States import *

class CheckCdkeyState(BaseState):

    mStateName = 'CheckCdkeyState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False