import socket,sys,threading,time

class SocketBaseModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def StartSocket(cls, name="Base"):
        cls.name = name
        cls.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cls.serverSocket.connect(('localhost', 3377))
            print("已连接上Server")
        except Exception:
            print(f"你在启动{name}前必须先启动Server!")
            input("按回车键关闭窗口. . .")
            sys.exit(0)

    def StartListenServer(self):
        serverThread = threading.Thread(target=self.HandleServer, args=(self.serverSocket,))
        serverThread.start()
        return True

    @classmethod
    def HandleServer(cls, serverSocket):
        cls.HeartSendToServer()
        while True:
            try:
                data = serverSocket.recv(2048)
                if not data:
                    break
                cls.LogHeadHandle(data.decode('utf-8'))
                # print("收到服务器心跳")
            except Exception as e:
                print(f"发生异常:{e}")
                break

    @classmethod
    def LogHeadHandle(cls, msg:str):
        head, content = msg.split("|||")
        if head in ["heart"]:
            cls.HeartSendToServer()
            return
    
    @classmethod
    def LogSendToServer(cls, level, msg):
        # 之后根据level对INFO ERROR等调整颜色
        if level == 'INFO':
            text = f"log|||\033[92m{level}\033[0m|{msg}|||"
            cls.serverSocket.send(text.encode())
        elif level == 'WARNING':
            text = f"log|||\033[93m{level}\033[0m|{msg}|||"
            cls.serverSocket.send(text.encode())
        elif level == 'ERROR':
            text = f"log|||\033[91m{level}\033[0m|{msg}|||"
            cls.serverSocket.send(text.encode())
        elif level == 'DEBUG':
            text = f"log|||\033[94m{level}\033[0m|{msg}|||"
            cls.serverSocket.send(text.encode())
        else:
            text = f"log|||{level}|{msg}|||"
            cls.serverSocket.send(text.encode())

    @classmethod
    def HeartSendToServer(cls):
        time.sleep(5)
        text = f"heart|||ClientOnline|||"
        cls.serverSocket.send(text.encode())

        
        