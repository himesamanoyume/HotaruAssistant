import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"{data.decode('utf-8')}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3377))
    server_socket.listen(5)
    print("服务器已启动，正在等待客户端连接...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"客户端{client_address}已连接")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
