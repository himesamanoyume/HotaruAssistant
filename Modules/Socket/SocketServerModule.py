import socket,threading,datetime
from Hotaru.Server.LogServerHotaru import logServerMgr


class SocketServerModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def StartSocket(cls):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('localhost', 3377))
        serverSocket.listen(0)
        logServerMgr.Info("服务器已启动，正在等待客户端连接...")
        while True:
            clientSocket, clientAddress = serverSocket.accept()
            logServerMgr.Info(f"客户端{clientAddress},已连接.")
            clientThread = threading.Thread(target=cls.HandleClient, args=(clientSocket,))
            clientThread.start()

    @classmethod
    def HandleClient(cls, clientSocket):
        # 可能需要记录连接的client到数据结构里,用于对指定client发送消息
        while True:
            try:
                data = clientSocket.recv(1024)
                if not data:
                    break
                cls.LogHeadHandle(data.decode('utf-8'))
            except Exception as e:
                logServerMgr.Error(f"发生异常:{e}")
                break
    
    @classmethod
    def LogHeadHandle(cls, content):
        currentTime = datetime.datetime.now()
        logServerMgr.Info(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]{content}")