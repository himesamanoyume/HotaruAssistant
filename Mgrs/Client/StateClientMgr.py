
from Hotaru.Client.LogClientHotaru import logMgr,log
from Mgrs.Base.StateBaseMgr import StateBaseMgr


class StateClientMgr(StateBaseMgr):
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls, logMgr, log)

        return cls.mInstance
