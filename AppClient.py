import sys,pyuac,atexit,os,questionary,shutil,datetime,time,threading
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Client.LogClientHotaru import logClientMgr,log
from Hotaru.Client.OcrClientHotaru import ocrClientMgr
from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.ConfigClientHotaru import configClientMgr
from Hotaru.Client.GameHotaru import gameMgr
from Hotaru.Client.DataHotaru import data

class AppClient:
    def Main(self):
        configClientMgr.IsAgreed2Disclaimer()
        ocrClientMgr.CheckPath()
        # gameMgr.SetupGame()
        gameMgr.DetectNewAccounts()

        if len(configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS]) == 0:
            log.warning(logClientMgr.Warning("你并没有填写注册表位置"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            gameLoopThread = threading.Thread(target=self.GameLoop)
            gameLoopThread.start()
        
        while True:
            time.sleep(5)
        # input("按回车键关闭窗口. . .")
        # sys.exit(0)

    def GameLoop(self):
        log.info(logClientMgr.Info("开始初始化循环列表"))
        optionsReg = dict()

        for index in range(len(configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS])):
            uidStr = str(configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS]).split('-')[1][:9]
            if uidStr in configClientMgr.mConfig[configClientMgr.mKey.BLACKLIST_UID]:
                log.warning(logClientMgr.Warning(f"{uidStr}【正在黑名单中】"))
                continue 
                
            gameMgr.ReadyToStart(uidStr)
            data.loginDict.update({f'{uidStr}' : f'{str(configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS][index])}'})
            data.loginList.append(f'{str(configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS][index])}')
            tempText = f":活跃度:{configClientMgr.mConfig[configClientMgr.mKey.DAILY_TASKS_SCORE] [uidStr]},模拟宇宙积分:{configClientMgr.mConfig[configClientMgr.mKey.UNIVERSE_SCORE] [uidStr]}"
            last_run_uidText = "【最后运行的账号】" if configClientMgr.mConfig[configClientMgr.mKey.LAST_RUNNING_UID] == uidStr else '' 
            optionsReg.update({("<每日已完成>" + uidStr + tempText + last_run_uidText
                                if configClientMgr.mConfig[configClientMgr.mKey.DAILY_TASKS_FIN][uidStr] 
                                else 
                                uidStr + tempText + last_run_uidText) : index})
            
        log.hr(logClientMgr.Hr("注意:选择轮次后将持续循环该轮次下的配置,不会出现轮次变更,因此建议直接选择全部轮次,若有单独轮次的需求可关闭后重新打开助手再进行选择"))

        optionsAction = {"全部轮次:每日任务轮次+模拟宇宙轮次(推荐)": "all", "单独每日任务轮次": "daily", "单独模拟宇宙轮次": "universe"}

        actionSelectTitle = "请选择进行的轮次:"
        actionSelectOption = questionary.select(actionSelectTitle, list(optionsAction.keys())).ask()
        selectedAction = optionsAction.get(actionSelectOption)

        regSelectTitle = "请选择UID进行作为首位启动游戏:"
        regSelectOption = questionary.select(regSelectTitle, list(optionsReg.keys())).ask()
        selectedReg = optionsReg.get(regSelectOption)
        
        log.info(logClientMgr.Info(f"进行轮次:{actionSelectOption}, 首个启动UID:{regSelectOption[:9]}"))

        isFirstTimeLoop = True

        while True:
            data.ResetData()
            if not os.path.exists("./backup"):
                os.makedirs("./backup")

            shutil.copy("./config.yaml",f"./backup/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.config.yaml")

            lastUID = str(data.loginList[len(data.loginList) - 1]).split('-')[1][:9]
            log.info(logClientMgr.Info(f"当前列表最后一个账号UID为:{lastUID}"))
            data.loopStartTimestamp = time.time()


def ExitHandler():
    # 退出 OCR
    ocrClientMgr.mOcr.ExitOcr()

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            log.error(logClientMgr.Error("管理员权限获取失败"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            atexit.register(ExitHandler)
            appClient = AppClient()
            appClient.Main()
        except KeyboardInterrupt:
            log.error(logClientMgr.Error("发生错误: 手动强制停止"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            log.error(logClientMgr.Error(f"发生错误: {e}"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)