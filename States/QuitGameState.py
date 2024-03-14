from States import *
from Hotaru.Client.GameControlHotaru import gameMgr
from Hotaru.Client.DataClientHotaru import dataMgr

class QuitGameState(BaseState):

    mStateName = 'QuitGameState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        gameMgr.StopGame()
        return False

    def OnExit(self):
        dataMgr.ResetData()
        return False
