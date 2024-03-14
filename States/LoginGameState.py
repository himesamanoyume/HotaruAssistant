from States import *
from Hotaru.Client.ScreenHotaru import screenMgr
from Modules.Utils.Retry import Retry

class LoginGameState(BaseState):

    mStateName = 'LoginGameState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
