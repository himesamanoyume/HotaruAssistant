from States import *
from .BaseRelicState import BaseRelicState

class GetRelicsInfoState(BaseRelicState, BaseState):

    mStateName = 'GetRelicsInfoState'

    def OnBegin(self):
        BaseRelicState.DetectRelicCount()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
