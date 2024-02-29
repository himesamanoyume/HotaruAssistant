import sys,pyuac,atexit,os
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Client.LogClientHotaru import logClientMgr
from Hotaru.Client.StateHotaru import stateMgr
from States.InitState import InitState

def main():
    
    stateMgr.Transition(InitState())
    # configClientMgr.SetConfigValue(configClientMgr.mConfig.mConfigKey.common.last_running_uid, value='111111112')
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
            main()
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