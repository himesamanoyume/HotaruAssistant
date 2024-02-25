import socket


class SocketServerModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def StartSocket():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 3377))
        server_socket.listen(0)
        # LogServerMgr.Log("服务器已启动，正在等待客户端连接...")
