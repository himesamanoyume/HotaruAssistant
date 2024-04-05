
from Mgrs.Base.SocketBaseMgr import SocketBaseMgr

class SocketClientMgr(SocketBaseMgr):
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls, "Client")

        return cls.mInstance
