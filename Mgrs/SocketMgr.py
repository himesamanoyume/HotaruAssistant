
from Modules.Socket.SocketClientModule import SocketClientModule
from Modules.Socket.SocketServerModule import SocketServerModule

class SocketMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mSocketClientModule = SocketClientModule()
            cls.mSocketServerModule = SocketServerModule()

        return cls.mInstance