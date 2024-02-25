
from Modules.Socket.SocketClientModule import SocketClientModule

class SocketClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mSocketClientModule = SocketClientModule()

        return cls.mInstance
    
    @classmethod
    def StartSocket(cls):
        cls.mSocketClientModule.StartSocket()