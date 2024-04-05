from States.Client import *
from .BaseRelicState import BaseRelicState

class GetRelicsInfoState(BaseRelicState, BaseClientState):

    mStateName = 'GetRelicsInfoState'

    def OnBegin(self):
        return BaseRelicState.DetectRelicCount()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
