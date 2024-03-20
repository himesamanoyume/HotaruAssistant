from States import *
from .BaseUniverseState import BaseUniverseState

class GetUniverseInfoState(BaseUniverseState, BaseState):

    mStateName = 'GetUniverseScoreState'

    def OnBegin(self):
        currentScore, maxScore = BaseUniverseState.GetUniverseScore()
        dataMgr.currentUniverseScore = currentScore
        dataMgr.maxCurrentUniverseScore = maxScore
        BaseUniverseState.GetUniverseReward()
        BaseUniverseState.GetImmersifier()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False

    
