import socket
import threading
import os
import requests
import json
import sys
from app import apprun

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"{data.decode('utf-8')}")
        except Exception as e:
            print(f"发生异常:{e}")
            break

def run_flask():
    apprun()
    # os.system("cmd /C flask run --debug --host=0.0.0.0")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3377))
    server_socket.listen(5)
    print("服务器已启动，正在等待客户端连接...")
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"客户端{client_address}已连接")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    r = requests.get("https://key.himesamanoyume.top/key.json")
    data = json.loads(r.text)
    if not data['key'] == 'zxcvbnm':
        input("KEY ERROR...")
        sys.exit(0)
    start_server()
