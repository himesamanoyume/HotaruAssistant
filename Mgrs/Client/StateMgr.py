
from States.BaseState import BaseState
from Hotaru.Client.LogClientHotaru import logClientMgr
import time


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
            time.sleep(0.5)
            cls.mCurrentState.OnExit()

        time.sleep(0.5)
        cls.mCurrentState = state
        logClientMgr.Info(f"状态已变换至:{state.mStateName}")

        if not cls.mCurrentState.OnBegin():
            time.sleep(0.5)
            cls.mCurrentState.OnRunning()
            time.sleep(0.5)

        return True
