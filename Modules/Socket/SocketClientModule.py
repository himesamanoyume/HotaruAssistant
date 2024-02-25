import socket,datetime,threading,os,requests,json,sys,questionary
from Mgrs.Client.LogClientMgr import logClientMgr

class SocketClientModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def StartSocket():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(('localhost', 3377))
            logClientMgr.Info("已连接上Server")
        except Exception:
            logClientMgr.Warning("你在启动Client前必须先启动Server!")
            input("按回车键关闭窗口. . .")
            sys.exit(0)