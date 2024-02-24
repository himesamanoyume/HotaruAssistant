import sys,pyuac,atexit,os
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Mgrs.HotaruServerMgr import logMgr,configMgr,stateMgr,clickMgr,jsonMgr,socketMgr,screenMgr,webMgr

def main():
    logMgr.Info("哈哈")
    # stateMgr.Transition(stateMgr.CompleteDailyState())
    input("test...")
    pass



if __name__ == "__main__":
    # if not pyuac.isUserAdmin():
    #     try:
    #         pyuac.runAsAdmin(wait=False)
    #         sys.exit(0)
    #     except Exception:
    #         # logger.error("管理员权限获取失败")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    # else:
        try:
            main()
            # atexit.register(exit_handler)
            # main(sys.argv[1]) if len(sys.argv) > 1 else main()
        except KeyboardInterrupt:
            logMgr.Error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logMgr.Error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)