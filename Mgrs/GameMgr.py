from Modules.Client.GameControllerModule import GameControllerModule
from Mgrs.HotaruClientMgr import LogClientMgr

class GameMgr:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mGameControllerModule = GameControllerModule()

        return cls.mInstance