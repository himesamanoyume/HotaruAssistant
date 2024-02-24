from States.State import State
from States.CompleteDailyState import CompleteDailyState
from States.InitState import InitState
from Mgrs.HotaruMgr import LogMgr

class StateMgr:
    mInstance = None
    mCurrentState = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.InitState()

        return cls.mInstance

    def Transition(cls, state: State):
        LogMgr.Info(f"To State:{state.mStateName}")
        cls.mCurrentState = state

    @staticmethod
    def InitState():
        state = InitState.Init()
        return state
    
    @staticmethod
    def CompleteDailyState():
        state = CompleteDailyState.Init()
        return state
