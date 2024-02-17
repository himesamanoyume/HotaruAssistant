from Mgrs.BaseMgr import BaseMgr
from States.BaseState import BaseState

class GameStateMgr(BaseMgr):
    mCurrentState = None
    

    def __init__(self):
        super().__init__()


    