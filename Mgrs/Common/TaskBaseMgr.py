class TaskBaseMgr:
    mInstance = None

    def __new__(cls, logMgr, log, stateMgr, dataMgr):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.logMgr = logMgr
            cls.log = log
            cls.stateMgr = stateMgr
            cls.dataMgr = dataMgr

        return cls.mInstance
