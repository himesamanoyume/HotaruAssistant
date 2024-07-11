from States.Client import *
from .BaseUniverseState import BaseUniverseState

class GetUniverseRewardAndInfoState(BaseUniverseState, BaseClientState):

    mStateName = 'GetUniverseRewardAndInfoState'

    def OnBegin(self):
        BaseUniverseState.GetDivergentUniverseReward()
        BaseUniverseState.GetDivergentUniverseImmersifier()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False

    
