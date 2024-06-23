from States.Client import *
from .BaseUniverseState import BaseUniverseState
from Hotaru.Client.ScreenClientHotaru import screenClientMgr

class GetUniverseRewardAndInfoState(BaseUniverseState, BaseClientState):

    mStateName = 'GetUniverseRewardAndInfoState'

    def OnBegin(self):
        BaseUniverseState.GetDivergentUniverseReward()
        BaseUniverseState.GetDivergentUniverseImmersifier()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False

    
