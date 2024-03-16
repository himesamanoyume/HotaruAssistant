from States import *
from Hotaru.Client.ScreenHotaru import screenMgr
from Modules.Utils.Retry import Retry

class LoginGameState(BaseState):

    mStateName = 'LoginGameState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        screenMgr.ShowDetectArea((50, 50, 200, 200))

    def OnExit(self):
        return False
