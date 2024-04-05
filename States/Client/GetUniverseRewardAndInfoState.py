from States.Client import *
from .BaseUniverseState import BaseUniverseState

class GetUniverseRewardAndInfoState(BaseUniverseState, BaseClientState):

    mStateName = 'GetUniverseRewardAndInfoState'

    def OnBegin(self):
        currentScore, maxScore = BaseUniverseState.GetUniverseReward()
        dataClientMgr.currentUniverseScore = currentScore
        dataClientMgr.maxCurrentUniverseScore = maxScore
        BaseUniverseState.GetImmersifier()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False

    
