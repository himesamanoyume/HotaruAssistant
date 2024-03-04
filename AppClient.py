import sys,pyuac,atexit,os,threading
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Client.LogClientHotaru import logClientMgr
from Hotaru.Client.StateHotaru import stateMgr
from States.InitState import InitState
from Hotaru.Client.OcrClientHotaru import ocrClientMgr
# from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.ConfigClientHotaru import configClientMgr

class AppClient:
    def Main(self):
        stateMgr.Transition(InitState())
        input("按回车键关闭窗口. . .")
        sys.exit(0)

def ExitHandler():
    # 退出 OCR
    ocrClientMgr.mOcr.ExitOcr()

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logClientMgr.Error("管理员权限获取失败")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            atexit.register(ExitHandler)
            appClient = AppClient()
            appClient.Main()
        except KeyboardInterrupt:
            logClientMgr.Error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logClientMgr.Error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)