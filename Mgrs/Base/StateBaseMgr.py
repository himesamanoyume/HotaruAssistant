
from States.Base.BaseState import BaseState
import time


class StateBaseMgr:
    mInstance = None
    mCurrentState:BaseState = None
    
    def __new__(cls, logMgr, log):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.logMgr = logMgr
            cls.log = log

        return cls.mInstance

    def Transition(cls, state: BaseState):
        cls.log.debug(cls.logMgr.Debug(f"状态将变换至:{state.mStateName}"))
        if not cls.mCurrentState is None:
            time.sleep(0.2)
            cls.log.debug(cls.logMgr.Debug(f"正在退出状态:{cls.mCurrentState.mStateName}"))
            cls.mCurrentState.OnExit()

        time.sleep(0.2)
        cls.mCurrentState = state
        cls.log.debug(cls.logMgr.Debug(f"状态已变换至:{state.mStateName}"))

        not2NextState = cls.mCurrentState.OnBegin()
        # 当OnBegin中返回值为True时,意味着该状态被强行打断,将不会执行OnRunning
        if not not2NextState:
            time.sleep(0.2)
            if not cls.mCurrentState.OnRunning():
                time.sleep(0.2)
            else:
                return True
        else:
            return not2NextState
