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
        configMgr.IsAgreed2Disclaimer() # 联系着自动保存 不能注释

        # updateMgr.mUpdate.DetectVersionUpdate()
        ocrServerMgr.CheckPath()
        logMgr.Hr(base64.b64decode("B|5YWs5ZGK".split('|')[1]).decode('utf-8'), 2)
        if dataMgr.YW5ub3VuY2VtZW50:
            for aWl0ZW1t in dataMgr.YW5ub3VuY2VtZW50:
                logMgr.Hr(f"【{aWl0ZW1t['Title']}】:{aWl0ZW1t['Content']}")
        else:
            logMgr.Error("{Y2NvbnRlbnR0}".format(Y2NvbnRlbnR0=base64.b64decode("5pyq6IO96I635Y+W5Yiw5YWs5ZGK").decode('utf-8')))
        webMgr.StartWeb()
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
            logMgr.Error(f"Main发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)