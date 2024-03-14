from States import *
from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.GameControlHotaru import gameMgr

class StartGameState(BaseState):

    mStateName = 'StartGameState'

    def OnBegin(self):
        return False
    
    def OnRunning(self):
        gameMgr.StartGame()
        return False

    def OnExit(self):
        return False
