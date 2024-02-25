
from Modules.Socket.SocketServerModule import SocketServerModule

class SocketServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mSocketServerModule = SocketServerModule()

        return cls.mInstance