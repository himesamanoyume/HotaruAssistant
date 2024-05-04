from States.Client import *
from .BaseRelicsState import BaseRelicsState

class GetRelicsInfoState(BaseRelicsState, BaseClientState):

    mStateName = 'GetRelicsInfoState'

    def OnBegin(self):
        return BaseRelicsState.DetectRelicsCount()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
