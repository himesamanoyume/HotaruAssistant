import socket,datetime,threading,os,requests,json,sys
from app import apprun

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            current_time = datetime.datetime.now()
            print(f"[{current_time.hour:02d}:{current_time.minute:02d}]{data.decode('utf-8')}")
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
    print("需要到下方显示的IP地址中进入后台")
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
