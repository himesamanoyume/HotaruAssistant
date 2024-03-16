
from States.BaseState import BaseState
from Hotaru.Client.LogClientHotaru import logMgr,log
import time


class StateMgr:
    mInstance = None
    mCurrentState:BaseState = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance

    def Transition(cls, state: BaseState):
        log.debug(logMgr.Debug(f"状态将变换至:{state.mStateName}"))
        if not cls.mCurrentState is None:
            time.sleep(0.5)
            log.debug(logMgr.Debug(f"正在退出状态:{cls.mCurrentState.mStateName}"))
            cls.mCurrentState.OnExit()

        time.sleep(0.5)
        cls.mCurrentState = state
        log.debug(logMgr.Debug(f"状态已变换至:{state.mStateName}"))

        isNextState = cls.mCurrentState.OnBegin()
        
        if not isNextState or isNextState is None:
            time.sleep(0.5)
            cls.mCurrentState.OnRunning()
            time.sleep(0.5)
        else:
            return isNextState
