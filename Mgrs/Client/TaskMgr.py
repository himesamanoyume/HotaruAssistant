
from Hotaru.Client.LogClientHotaru import logMgr,log
from Task.Base.Base import Base

class TaskMgr:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance
    
    @staticmethod
    def SetupGame():
        Base.SetupGame()

    @staticmethod
    def StopGame():
        pass

    @staticmethod
    def DetectNewAccounts():
        Base.DetectNewAccount()

    @staticmethod
    def ReadyToStart(uid):
        Base.ReadyToStart(uid)

    @staticmethod
    def StartDaily(expectUid, lastUid):
        pass

    @staticmethod
    def StartUniverse(expectUid, lastUid):
        pass