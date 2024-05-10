from States.Client import *
from .BaseUniverseState import BaseUniverseState

class GetUniverseRewardAndInfoState(BaseUniverseState, BaseClientState):

    mStateName = 'GetUniverseRewardAndInfoState'

    def OnBegin(self):
        BaseUniverseState.GetUniverseReward()
        BaseUniverseState.GetImmersifier()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False

    
