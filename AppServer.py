import sys,pyuac,atexit,os
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Server.LogServerHotaru import logServerMgr
from Hotaru.Server.ConfigServerHotaru import configServerMgr
from Hotaru.Server.WebHotaru import webMgr
from Hotaru.Server.SocketServerHotaru import socketServerMgr
from Hotaru.Server.UpdateHotaru import updateMgr

class AppServer:
    def Main():
        configServerMgr.IsAgreeDisclaimer()
        updateMgr.DetectVersionUpdate()
        # logServerMgr.Info("哈哈")
        webMgr.StartWeb()
        socketServerMgr.StartSocket()

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logServerMgr.Error("管理员权限获取失败")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            AppServer.Main()
            # atexit.register(exit_handler)
            # main(sys.argv[1]) if len(sys.argv) > 1 else main()
        except KeyboardInterrupt:
            logServerMgr.Error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logServerMgr.Error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)