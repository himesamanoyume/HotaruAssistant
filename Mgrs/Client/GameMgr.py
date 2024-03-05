
from Hotaru.Client.LogClientHotaru import logClientMgr
from Game.Setup.SetupGame import SetupGame

class GameMgr:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance
    
    @staticmethod
    def SetupGame():
        SetupGame.SetupGame()
        