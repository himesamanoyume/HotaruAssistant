import socket,datetime,threading,os,requests,json,sys,questionary
from app import apprun
from module.config.config import Config
config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")

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
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"客户端{client_address}已连接")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def show_disclaimer():
    print("《免责声明》")
    print("本软件是一个外部工具旨在自动化崩坏星轨的游戏玩法。它被设计成仅通过现有用户界面与游戏交互,并遵守相关法律法规。该软件包旨在提供简化和用户通过功能与游戏交互,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。")
    print("This software is open source, free of charge and for learning and exchange purposes only. The developer team has the final right to interpret this project. All problems arising from the use of this software are not related to this project and the developer team. If you encounter a merchant using this software to practice on your behalf and charging for it, it may be the cost of equipment and time, etc. The problems and consequences arising from this software have nothing to do with it.")
    print("本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。")
    print("根据MiHoYo的 [崩坏:星穹铁道的公平游戏宣言]：")
    print('"严禁使用外挂、加速器、脚本或其他破坏游戏公平性的第三方工具。"')
    print('"一经发现，米哈游（下亦称“我们”）将视违规严重程度及违规次数，采取扣除违规收益、冻结游戏账号、永久封禁游戏账号等措施。"')
    title_ = "你是否接受?"
    options = dict()
    options.update({"我接受":0})
    options.update({"我拒绝":1})
    option_ = questionary.select(title_, list(options.keys())).ask()
    value = options.get(option_)
    if value == 0:
        config.set_value("agreed_to_disclaimer", True)
    else:
        print("您未同意《免责声明》")
        input("按回车键关闭窗口. . .")
        sys.exit(0)
    

def agreed_to_disclaimer():
    # 免责申明
    if not config.agreed_to_disclaimer:
        show_disclaimer()

if __name__ == "__main__":
    agreed_to_disclaimer()
    start_server()
