
from States.BaseState import BaseState
# from States.CompleteDailyState import CompleteDailyState
# from States.InitState import InitState
from Hotaru.Client.LogClientHotaru import logClientMgr


class StateMgr:
    mInstance = None
    mCurrentState:BaseState = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance

    def Transition(cls, state: BaseState):
        logClientMgr.Info(f"状态将变换至:{state.mStateName}")
        if not cls.mCurrentState is None:
            cls.mCurrentState.OnExit()

        cls.mCurrentState = state
        logClientMgr.Info(f"状态已变换至:{state.mStateName}")

        if not cls.mCurrentState.OnBegin():
            cls.mCurrentState.OnRunning()
