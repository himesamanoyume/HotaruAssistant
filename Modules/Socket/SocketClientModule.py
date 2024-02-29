import socket,sys,threading,datetime

class SocketClientModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def StartSocket(cls):
        cls.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cls.clientSocket.connect(('localhost', 3377))
            print("已连接上Server")
        except Exception:
            print("你在启动Client前必须先启动Server!")
            input("按回车键关闭窗口. . .")
            sys.exit(0)

    @classmethod
    def LogSendToServer(cls, level, uid, action, msg):
        # 之后根据level对INFO ERROR等调整颜色
        text = f"{level}|\033[91m[{uid}]\033[0m|{action}|{msg}"
        cls.clientSocket.send(text.encode())