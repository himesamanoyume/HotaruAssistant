import sys,pyuac,atexit,os,questionary,shutil,datetime,time,threading
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.OcrHotaru import ocrMgr
from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.TaskHotaru import taskMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from Hotaru.Client.SocketClientHotaru import socketClientMgr


class AppClient:
    def Main(self):
        socketClientMgr.StartListenServer()
        configMgr.IsAgreed2Disclaimer()
        ocrMgr.CheckPath()
        taskMgr.DetectNewAccounts()

        if len(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS]) == 0:
            log.warning(logMgr.Warning("你并没有填写注册表位置"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            hotaruLoopThread = threading.Thread(target=self.HotaruAssistantLoop)
            hotaruLoopThread.start()
        

        while dataMgr.currentGamePid == -1:
            time.sleep(5)

        screenLoopThread = threading.Thread(target=screenMgr.StartDevScreen)
        screenLoopThread.start()

    def HotaruAssistantLoop(self):
        dataMgr.gameTitleName = configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]
        log.info(logMgr.Info("开始初始化循环列表"))
        optionsReg = dict()

        for index in range(len(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS])):

            uidStr = str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index]).split('-')[1][:9]
            if uidStr in configMgr.mConfig[configMgr.mKey.BLACKLIST_UID]:
                log.warning(logMgr.Warning(f"{uidStr}【正在黑名单中】"))
                continue 
                
            taskMgr.ReadyToStart(uidStr)
            dataMgr.loginDict.update({f'{uidStr}' : f'{str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index])}'})
            dataMgr.loginList.append(f'{str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index])}')

            tempText = f":活跃度:{configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][uidStr]},模拟宇宙积分:{configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][uidStr]}"

            last_run_uidText = "【最后运行的账号】" if configMgr.mConfig[configMgr.mKey.LAST_RUNNING_UID] == uidStr else '' 
            optionsReg.update({("<每日已完成>" + uidStr + tempText + last_run_uidText
                                if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][uidStr] 
                                else 
                                uidStr + tempText + last_run_uidText) : index})
            
        log.hr(logMgr.Hr("注意:选择轮次后将持续循环该轮次下的配置,不会出现轮次变更,因此建议若有单独轮次的需求可关闭后重新打开助手再进行选择"))

        optionsAction = {"全部轮次:每日任务轮次+模拟宇宙轮次": "all", "单独每日任务轮次": "daily", "单独模拟宇宙轮次": "universe"}

        actionSelectTitle = "请选择进行的轮次:\n"
        actionSelectOption = questionary.select(actionSelectTitle, list(optionsAction.keys())).ask()
        selectedAction = optionsAction.get(actionSelectOption)

        regSelectTitle = "请选择UID进行作为首位启动游戏:\n"
        regSelectOption = questionary.select(regSelectTitle, list(optionsReg.keys())).ask()
        selectedReg = optionsReg.get(regSelectOption)
        
        log.info(logMgr.Info(f"进行轮次:{actionSelectOption}, 首个启动UID:{regSelectOption}"))

        isFirstTimeLoop = True

        if not os.path.exists("./backup"):
            os.makedirs("./backup")

        shutil.copy("./config.yaml",f"./backup/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.config.yaml")

        while True:
            dataMgr.ResetData()
            
            lastUID = str(dataMgr.loginList[len(dataMgr.loginList) - 1]).split('-')[1][:9]
            log.info(logMgr.Info(f"当前列表最后一个账号UID为:{lastUID}"))
            dataMgr.loopStartTimestamp = time.time()

            firstTimeLogin = True
            jumpValue = ''
            jumpFin = False

            if selectedAction == 'all':
                count = 2
            else:
                count = 1

            for turn in range(count):

                for regStr in dataMgr.loginList:
                    if not firstTimeLogin and not jumpFin:
                        if not regStr == jumpValue:
                            continue
                        else:
                            jumpFin = True

                    uidStr2 = str(regStr).split('-')[1][:9]
                    taskMgr.DetectNewAccounts()

                    if isFirstTimeLoop:
                        if firstTimeLogin:
                            firstTimeLogin = False
                            jumpValue = dataMgr.loginList[selectedReg]
                            if jumpValue == regStr:
                                jumpFin = True
                            else:
                                continue
                    
                    log.info(logMgr.Info(f"运行命令: cmd /C REG IMPORT {regStr}"))
                    if os.system(f"cmd /C REG IMPORT {regStr}"):
                        input("导入注册表出错,检查对应注册表路径和配置是否正确,按回车键退出...")
                        return False
                    try:
                        if count == 1:
                            if selectedAction == 'daily':
                                if taskMgr.StartGame():
                                    dataMgr.currentAction = "每日任务流程"
                                    taskMgr.StartDaily()
                            elif selectedAction == 'universe':
                                if taskMgr.StartGame():
                                    dataMgr.currentAction = "模拟宇宙流程"
                                    taskMgr.StartUniverse()
                        else:
                            if turn == 0:
                                if taskMgr.StartGame():
                                    dataMgr.currentAction = "每日任务流程"
                                    taskMgr.StartDaily()
                            else:
                                if not dataMgr.isDetectUniverseScoreAndFinished or configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uidStr2] == '模拟宇宙':
                                    if taskMgr.StartGame():
                                        dataMgr.currentAction = "模拟宇宙流程"
                                        taskMgr.StartUniverse()

                                    dataMgr.isDetectUniverseScoreAndFinished = False

                        taskMgr.SendNotify()
                        taskMgr.QuitGame()
                    except Exception as e:
                        taskMgr.SendExceptionNotify()
                        taskMgr.QuitGame()

            taskMgr.WaitForNextLoop()



def ExitHandler():
    # 退出 OCR
    ocrMgr.mOcr.ExitOcr()

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            log.error(logMgr.Error("管理员权限获取失败"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            atexit.register(ExitHandler)
            appClient = AppClient()
            appClient.Main()
        except KeyboardInterrupt:
            log.error(logMgr.Error("发生错误: 手动强制停止"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            log.error(logMgr.Error(f"发生错误: {e}"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)