
from Mgrs.SocketClientSubMgr import SocketClientSubMgr
from Mgrs.SocketServerSubMgr import SocketServerSubMgr

class SocketMgr:
    
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mInstance.mClientMgr = SocketClientSubMgr(logMgr)
            cls.mInstance.mServerMgr = SocketServerSubMgr(logMgr)
        return cls.mInstance