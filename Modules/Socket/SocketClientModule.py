import socket,datetime,threading,os,requests,json,sys,questionary
from Mgrs.HotaruClientMgr import LogClientMgr

class SocketClientModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def StartSocket():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 3377))
        server_socket.listen(0)
        LogClientMgr.Info("")