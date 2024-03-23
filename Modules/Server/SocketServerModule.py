import socket,threading,datetime
from Hotaru.Server.LogServerHotaru import logMgr
from Hotaru.Server.DataServerHotaru import dataMgr

class SocketServerModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def StartSocket(cls):
        cls.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.serverSocket.bind(('localhost', 3377))
        cls.serverSocket.listen(0)
        logMgr.Info("服务器已启动，正在等待客户端连接...")
        accpetClientThread = threading.Thread(target=cls.AcceptClient, args=())
        accpetClientThread.start()

    @classmethod
    def AcceptClient(cls):
        # 可能需要记录连接的client到数据结构里,用于对指定client发送消息
        while True:
            clientSocket, clientAddress = cls.serverSocket.accept()
            logMgr.Info(f"客户端{clientAddress},已连接.")
            dataMgr.clientDict.update({clientSocket : clientAddress})
            clientThread = threading.Thread(target=cls.HandleClient, args=(clientSocket,))
            clientThread.start()

    @classmethod
    def HandleClient(cls, clientSocket):
        while True:
            try:
                data = clientSocket.recv(1024)
                if not data:
                    break
                cls.LogHeadHandle(data.decode('utf-8'), clientSocket)
            except Exception as e:
                logMgr.Error(f"处理Client消息发生异常:{e}")
                return
    
    @staticmethod
    def HeartSendToClient(clientSocket):
        text = f"heart|||ServerOnline"
        clientSocket.send(text.encode())
            
    @classmethod
    def LogHeadHandle(cls, msg:str, clientSocket):
        temp = msg.split("|||")
        head = temp[0]
        content = temp[1]
        if len(temp) > 2 and len(temp) % 2 == 0:
            for i in range(len(temp) - 2):
                if temp[i+2] in ["log"]:
                    logMgr.Socket(f"{temp[i+3]}")
                    return
                elif temp[i+2] in ["heart"]:
                    # print(f"收到客户端{data.clientDict[clientSocket]}心跳")
                    cls.HeartSendToClient(clientSocket)
                    return
        
        if head in ["log"]:
            logMgr.Socket(f"{content}")
            return
        elif head in ["heart"]:
            # print(f"收到客户端{data.clientDict[clientSocket]}心跳")
            cls.HeartSendToClient(clientSocket)
            return

        