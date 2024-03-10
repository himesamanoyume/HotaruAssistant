import sys,pyuac,atexit,os,time,base64
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Server.LogServerHotaru import logMgr
from Hotaru.Server.ConfigServerHotaru import configMgr
from Hotaru.Server.WebHotaru import webMgr
from Hotaru.Server.SocketServerHotaru import socketServerMgr
from Hotaru.Server.UpdateHotaru import updateMgr
from Hotaru.Server.OcrServerHotaru import ocrServerMgr
from Hotaru.Server.DataServerHotaru import dataMgr

class AppServer:
    @staticmethod
    def Main():
        logMgr.Hr("HotaruAssistant - Server\n启动!")
        configMgr.IsAgreed2Disclaimer()
        # updateMgr.mUpdate.DetectVersionUpdate()
        ocrServerMgr.CheckPath()
        # logMgr.Hr(base64.b64decode("B|5YWs5ZGK".split('|')[1]).decode('utf-8'), 2)
        # for aWl0ZW1t in dataMgr.YW5ub3VuY2VtZW50:
        #     logMgr.Hr(f"【{aWl0ZW1t['Title']}】:{aWl0ZW1t['Content']}")
        webMgr.StartWeb()
        # webMgr.StartDebugWeb()
        socketServerMgr.StartSocket()
        

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logMgr.Error("管理员权限获取失败")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            appServer = AppServer()
            appServer.Main()
        except KeyboardInterrupt:
            logMgr.Error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logMgr.Error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)