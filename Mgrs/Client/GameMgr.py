
from Hotaru.Client.LogClientHotaru import logClientMgr
from Game.Base.Base import Base

class GameMgr:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance
    
    @staticmethod
    def SetupGame():
        Base.SetupGame()

    @staticmethod
    def DetectNewAccounts():
        Base.DetectNewAccount()

    @staticmethod
    def ReadyToStart(uid):
        Base.ReadyToStart(uid)
        