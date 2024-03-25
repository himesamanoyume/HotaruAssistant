from States import *
from .BaseUniverseState import BaseUniverseState

class GetUniverseRewardAndInfoState(BaseUniverseState, BaseState):

    mStateName = 'GetUniverseRewardAndInfoState'

    def OnBegin(self):
        currentScore, maxScore = BaseUniverseState.GetUniverseReward()
        dataMgr.currentUniverseScore = currentScore
        dataMgr.maxCurrentUniverseScore = maxScore
        BaseUniverseState.GetImmersifier()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False

    
