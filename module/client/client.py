import socket

class Client:
    _instance = None
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.connect(('localhost', 3377))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls.c_socket

    # def start_client():
    #     c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     c_socket.connect(('localhost', 3377))
        # while True:
        #     message = input("请输入消息：")
        #     client_socket.send(message.encode('utf-8'))
