import sys,pyuac,atexit,os,threading
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Client.LogClientHotaru import logClientMgr
from Hotaru.Client.OcrClientHotaru import ocrClientMgr
# from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.ConfigClientHotaru import configClientMgr
from Hotaru.Client.GameHotaru import gameMgr
from Game.Base.Base import Base

class AppClient:
    def Main(self):
        configClientMgr.mConfig.IsAgreed2Disclaimer()
        ocrClientMgr.CheckPath()
        # gameMgr.SetupGame()
        gameMgr.DetectNewAccounts()

        if len(configClientMgr.GetConfigValue(configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS, None)) == 0:
            logClientMgr.Warning("你并没有填写注册表位置")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            logClientMgr.Info("开始多账号运行")
            options_reg = dict()

            for index in range(len(configClientMgr.GetConfigValue(configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS, None))):
                uidStr = str(configClientMgr.GetConfigValue(configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS, None)).split('-')[1][:9]
                if uidStr in configClientMgr.GetConfigValue(configClientMgr.mKey.BLACKLIST_UID, None):
                    logClientMgr.Warning(f"{uidStr}【正在黑名单中】")
                    continue
                
                gameMgr.ReadyToStart(uidStr)


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