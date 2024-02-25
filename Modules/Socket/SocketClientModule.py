import socket,sys
from Hotaru.Client.LogClientHotaru import logClientMgr

class SocketClientModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @staticmethod
    def StartSocket():
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clientSocket.connect(('localhost', 3377))
            logClientMgr.Info("已连接上Server")
        except Exception:
            logClientMgr.Warning("你在启动Client前必须先启动Server!")
            input("按回车键关闭窗口. . .")
            sys.exit(0)