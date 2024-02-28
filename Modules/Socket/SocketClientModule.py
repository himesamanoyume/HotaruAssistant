import socket,sys,threading,datetime
from Hotaru.Client.LogClientHotaru import logClientMgr

class SocketClientModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def StartSocket(cls):
        cls.__clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cls.__clientSocket.connect(('localhost', 3377))
            logClientMgr.Info("已连接上Server")
            # serverSocket, serverAddress = clientSocket.accept()
            # serverThread = threading.Thread(target=cls.HandleServer, args=(serverSocket,))
            # serverThread.start()
        except Exception:
            logClientMgr.Warning("你在启动Client前必须先启动Server!")
            input("按回车键关闭窗口. . .")
            sys.exit(0)

    @classmethod
    def LogSendToServer(cls, uid, action, msg):
        text = f"\033[91m[{uid}]033[0m|{action}|{msg}"
        cls.__clientSocket.send(text.encode())

    # @classmethod
    # def HandleServer(cls, serverSocket):
    #     while True:
    #         try:
    #             data = serverSocket.recv(1024)
    #             if not data:
    #                 break
    #             head, content = (data.decode('utf-8')).split('|')
    #             if head in ['config']:
    #                 cls.ConfigHeadHandle(content)
    #             elif head in ['log']:
    #                 cls.LogHeadHandle(content)
    #         except Exception as e:
    #             logClientMgr.Error(f"发生异常:{e}")
    #             break
    
    # @classmethod
    # def ConfigHeadHandle(cls, content):
    #     pass
    
    # @classmethod
    # def LogHeadHandle(cls, content):
    #     pass