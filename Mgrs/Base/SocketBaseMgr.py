
from Modules.Common.SocketBaseModule import SocketBaseModule

class SocketBaseMgr:
    mInstance = None
    
    def __new__(cls, name):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mSocketBaseModule = SocketBaseModule()
            cls.StartSocket(name)

        return cls.mInstance
    
    def StartListenServer(self):
        self.mSocketBaseModule.StartListenServer()
    
    @classmethod
    def StartSocket(cls, name = "Base"):
        cls.mSocketBaseModule.StartSocket(name)

    @classmethod
    def LogSendToServer(cls, level, msg):
        cls.mSocketBaseModule.LogSendToServer(level, msg)

    @classmethod
    def LogHeartSendToServer(cls):
        cls.mSocketBaseModule.HeartSendToServer()
