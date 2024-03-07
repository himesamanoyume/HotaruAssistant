
from Modules.Client.SocketClientModule import SocketClientModule

class SocketClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mSocketClientModule = SocketClientModule()
            cls.StartSocket()

        return cls.mInstance
    
    @classmethod
    def StartSocket(cls):
        cls.mSocketClientModule.StartSocket()

    @classmethod
    def LogSendToServer(cls, level, msg):
        cls.mSocketClientModule.LogSendToServer(level, msg)

    @classmethod
    def LogScreenSendToServer(cls, msg):
        cls.mSocketClientModule.LogScreenSendToServer(msg)
