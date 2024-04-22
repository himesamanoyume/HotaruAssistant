
from Modules.Common.SocketBaseModule import SocketBaseModule
import socket

class SocketBaseMgr:
    mInstance = None
    
    def __new__(cls, name):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mSocketBaseModule = SocketBaseModule()
            cls.StartSocket(name)
            cls.mIsConnected = False

        return cls.mInstance
    
    def StartListenServer(self):
        self.mIsConnected = self.mSocketBaseModule.StartListenServer()
    
    @classmethod
    def StartSocket(cls, name = "Base"):
        cls.mSocketBaseModule.StartSocket(name)

    @classmethod
    def LogSendToServer(cls, level, msg):
        if cls.mSocketBaseModule.serverSocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) == 0 and cls.mIsConnected:
            cls.StartSocket(cls.mSocketBaseModule.name)
            cls.mSocketBaseModule.StartListenServer()

        cls.mSocketBaseModule.LogSendToServer(level, msg)

    @classmethod
    def LogHeartSendToServer(cls):
        if cls.mSocketBaseModule.serverSocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) == 0 and cls.mIsConnected:
            cls.StartSocket(cls.mSocketBaseModule.name)
            cls.mSocketBaseModule.StartListenServer()

        cls.mSocketBaseModule.HeartSendToServer()
