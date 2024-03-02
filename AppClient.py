import sys,pyuac,atexit,os
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Client.LogClientHotaru import logClientMgr
from Hotaru.Client.StateHotaru import stateMgr
from States.InitState import InitState

class AppClient:
    def Main():
        stateMgr.Transition(InitState())
        input("test...")



if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            # logger.error("管理员权限获取失败")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            AppClient.Main()
            # atexit.register(exit_handler)
            # main(sys.argv[1]) if len(sys.argv) > 1 else main()
        except KeyboardInterrupt:
            logClientMgr.Error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logClientMgr.Error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)