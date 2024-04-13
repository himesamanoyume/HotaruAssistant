import sys,pyuac,atexit,os,questionary,shutil,datetime,time,threading,pyautogui
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.OcrClientHotaru import ocrClientMgr
from Hotaru.Client.ScreenClientHotaru import screenClientMgr
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.TaskClientHotaru import taskClientMgr
from Hotaru.Client.DataClientHotaru import dataClientMgr
from Hotaru.Client.SocketClientHotaru import socketClientMgr


class AppClient:
    def Main(self):
        socketClientMgr.StartListenServer()
        self.IsAgreed2Disclaimer()
        ocrClientMgr.CheckPath()
        taskClientMgr.DetectNewAccounts()

        if len(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS]) == 0:
            log.warning(logMgr.Warning("你并没有填写注册表位置"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            hotaruLoopThread = threading.Thread(target=self.HotaruAssistantLoop)
            hotaruLoopThread.start()
        

        while dataClientMgr.currentGamePid == -1:
            time.sleep(5)

        screenLoopThread = threading.Thread(target=screenClientMgr.StartDevScreen)
        screenLoopThread.start()

    def HotaruAssistantLoop(self):
        dataClientMgr.gameTitleName = configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]
        log.info(logMgr.Info("开始初始化循环列表"))
        optionsReg = dict()

        for index in range(len(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS])):

            uidStr = str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index]).split('-')[1][:9]
            if uidStr in configMgr.mConfig[configMgr.mKey.BLACKLIST_UID]:
                log.warning(logMgr.Warning(f"{uidStr}【正在黑名单中】"))
                continue 
                
            taskClientMgr.ReadyToStart(uidStr)
            dataClientMgr.loginDict.update({f'{uidStr}' : f'{str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index])}'})
            dataClientMgr.loginList.append(f'{str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index])}')

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
            dataClientMgr.ResetData()
            
            lastUID = str(dataClientMgr.loginList[len(dataClientMgr.loginList) - 1]).split('-')[1][:9]
            log.info(logMgr.Info(f"当前列表最后一个账号UID为:{lastUID}"))

            firstTimeLogin = True
            jumpValue = ''
            jumpFin = False

            if selectedAction == 'all':
                count = 2
            else:
                count = 1

            for turn in range(count):

                for regStr in dataClientMgr.loginList:
                    if not firstTimeLogin and not jumpFin:
                        if not regStr == jumpValue:
                            continue
                        else:
                            jumpFin = True

                    uidStr2 = str(regStr).split('-')[1][:9]
                    taskClientMgr.DetectNewAccounts()

                    if isFirstTimeLoop:
                        if firstTimeLogin:
                            firstTimeLogin = False
                            jumpValue = dataClientMgr.loginList[selectedReg]
                            if jumpValue == regStr:
                                jumpFin = True
                            else:
                                continue
                    else:
                        taskClientMgr.ReadyToStart(uidStr2)
                    
                    log.info(logMgr.Info(f"运行命令: cmd /C REG IMPORT {regStr}"))
                    if os.system(f"cmd /C REG IMPORT {regStr}"):
                        input("导入注册表出错,检查对应注册表路径和配置是否正确,按回车键退出...")
                        return False
                    try:
                        if count == 1:
                            if selectedAction == 'daily':
                                if taskClientMgr.ClientStartGame():
                                    dataClientMgr.currentAction = "每日任务流程"
                                    # raise Exception("测试异常")
                                    taskClientMgr.StartDaily()
                            elif selectedAction == 'universe':
                                if taskClientMgr.ClientStartGame():
                                    dataClientMgr.currentAction = "模拟宇宙流程"
                                    taskClientMgr.StartUniverse()

                            taskClientMgr.SendNotify()
                            taskClientMgr.QuitGame()
                        else:
                            if turn == 0:
                                if taskClientMgr.ClientStartGame():
                                    dataClientMgr.currentAction = "每日任务流程"
                                    taskClientMgr.StartDaily()
                                    taskClientMgr.SendNotify()
                                    taskClientMgr.QuitGame()
                            else:
                                if not dataClientMgr.isDetectUniverseScoreAndFinished or configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uidStr2] == '模拟宇宙':
                                    if taskClientMgr.ClientStartGame():
                                        dataClientMgr.currentAction = "模拟宇宙流程"
                                        taskClientMgr.StartUniverse()

                                    dataClientMgr.isDetectUniverseScoreAndFinished = False
                                    taskClientMgr.SendNotify()
                                    taskClientMgr.QuitGame()

                        
                    except Exception as e:
                        log.error(logMgr.Error(e))
                        taskClientMgr.SendExceptionNotify(e)
                        taskClientMgr.QuitGame()

            isFirstTimeLoop = False
            taskClientMgr.WaitForNextLoop()

    def IsAgreed2Disclaimer(self):
        if not configMgr.mConfig[configMgr.mKey.AGREED_TO_DISCLAIMER]:
            log.error(logMgr.Error("你未同意《免责声明》, 需要先启动Server并同意"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            self.autoSaveThread = threading.Thread(target=self.AutoSave)
            self.autoSaveThread.start()

    def AutoSave(self):
        while True:
            time.sleep(4)
            nowtime = time.time()
            if nowtime - configMgr.mConfig.mLastTimeSaveTimestamp >= 5 and nowtime - configMgr.mConfig.mLastTimeModifyTimestamp <= 10:
                configMgr.mConfig.SaveConfig()
                logMgr.Info("Client:配置文件进行自动保存")

class AppTools:
    def Main(self):
        socketClientMgr.StartListenServer()
        dataClientMgr.gameTitleName = configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]
        log.hr(logMgr.Hr("在进行选择前,需要通读对应选项下的说明,若注册表修改操作不当可能导致游戏画面等设置全部被清空!!!本人概不负责", True))
        input("按回车进行下一步")
        log.hr(logMgr.Hr("1.如果需要使用工具箱获取注册表,则需要先手动把游戏退出!!!使用工具箱截图则不需要", True))
        input("现在请手动关闭游戏,之后按回车进行下一步")
        log.hr(logMgr.Hr("2.检查config.yaml中的game_path是否正确填入!!!", True))
        input("按回车进行下一步")
        log.hr(logMgr.Hr("3.在启动游戏前确保桌面分辨率调整为1920*1080!!!注意是桌面分辨率而不是游戏分辨率", True))
        input("按回车进行下一步")
        title_ = "若已经关闭游戏,用方向键然后回车键选择你要做的:"
        options_reg = dict()
        options_reg.update({"0:选择获取新的注册表":0})
        options_reg.update({"1:选择重新导入完整注册表(导入注册表后需要重启游戏才会生效)":1})
        options_reg.update({"2:进行截图":2})
        option_ = questionary.select(title_, list(options_reg.keys())).ask()
        value = options_reg.get(option_)
        if value == 0:
            AppTools.RegistryExport()
        elif value == 1:
            AppTools.RestoreRegistry()
        elif value == 2:
            AppTools.TakeScreenshotFirst()
        
        input("按回车键关闭窗口. . .")
        sys.exit(0)
    
    def TakeScreenshotFirst():
        AppTools.TakeScreenshot()
        AppTools.ContinueTakeScreenshot()

    def ContinueTakeScreenshot():
        options_reg2 = dict()
        options_reg2.update({"0:继续截图":0})
        options_reg2.update({"1:退出":1})
        option_ = questionary.select("截图已完成,选择下一步", list(options_reg2.keys())).ask()
        value = options_reg2.get(option_)
        if value == 0:
            AppTools.TakeScreenshotFirst()
        else:
            pass

    def RestoreRegistry():
        log.info(logMgr.Info("正在重新导入完整注册表"))
        os.system(f"cmd /C reg import ./reg/temp-full.reg")

    def TakeScreenshot():
        if screenClientMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]):
            result = screenClientMgr.TakeScreenshot()
            if result:
                root = tk.Tk()
                app = ScreenshotApp(root, screenClientMgr.mDetect.screenshot)
                root.mainloop()

    def RegistryExport():
        try:
            log.hr(logMgr.Hr("[获取新的注册表]:操作步骤以及注意事项", True))
            log.hr(logMgr.Hr("1.本次操作会先保存当前的全部注册表(位于根目录./reg文件夹中,名称为temp-full.reg),之后再清空注册表,再启动游戏", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("2.清空注册表后游戏的设置都会重置,启动游戏时会以全屏状态进入,因此需要提前确保桌面分辨率为1920*1080", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("2.a.若担心操作不当,可以再把temp-full.reg备份到其他位置,每次进行【获取新的注册表】时都会覆盖temp-full.reg,操作不当可能会导致没有任何内容的注册表覆盖掉temp-full.reg的情况发生", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("3.启动游戏后,需要在10分钟内输入账号密码登录,否则判定为启动游戏失败", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("4.登录完成之后可以不点击进入游戏,脚本将自动识别进入游戏按钮,进入游戏后会自动识别UID,如果识别错误也可自行输入", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("5.然后你将获得对应UID账号的注册表文件(位于根目录./reg文件夹中,名称为starrail-xxxxxxxxx.reg)", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("6.退出游戏,关闭程序再重新运行工具箱,选择重新导入注册表,或直接双击temp-full.reg导入注册表,即可完成", True))
            input("若已阅读完毕,按回车开始获取注册表")
            # 保存完整的注册表
            log.info(logMgr.Info("正在保存完整的注册表"))
            if not os.path.exists("./reg"):
                os.makedirs("./reg")
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 ./reg/temp-full.reg /y")
            # 删除所有注册表
            log.info(logMgr.Info("正在删除所有注册表"))
            os.system(f"cmd /C reg delete HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 /f")
            input("此刻已生成temp-full.reg文件,你可以选择在这个空档进行文件备份,或按回车正式开始启动游戏...")
            # 等待游戏启动并登录
            if taskClientMgr.ToolsStartGame():
                log.info(logMgr.Info(f"识别UID:{dataClientMgr.currentUid},是否正确?根据情况选择下列选项:"))
                pyautogui.hotkey('alt', 'tab')
                options_reg2 = dict()
                options_reg2.update({f"正确,直接导出":0})
                options_reg2.update({"错误,手动输入UID":1})
                option_ = questionary.select(f"识别UID:{dataClientMgr.currentUid},是否正确?根据情况选择下列选项:", list(options_reg2.keys())).ask()
                pyautogui.hotkey('alt', 'tab')
                value = options_reg2.get(option_)
                if value == 0:
                    uid = dataClientMgr.currentUid
                elif value == 1:
                    uid = input("手动输入UID:\n")
                # end
                # 导出对应账号注册表
                log.info("导出对应账号注册表")
                os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 ./reg/starrail-{uid}.reg /y")
                # 重新导入完整注册表
                log.info("重新导入完整注册表")
                os.system(f"cmd /C reg import ./reg/temp-full.reg")
                log.info("完成,你已可以退出游戏,若要激活账号,需要到WEB后台的注册界面进行")
                pyautogui.hotkey('alt', 'tab')
            else:
                log.error(logMgr.Error(f"启动游戏超时"))
                input("按回车键关闭窗口. . .")
                sys.exit(0)

        except Exception as e:
            log.error(logMgr.Error(f"发生错误: {e}"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)

import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os,atexit

class ScreenshotApp:
    def __init__(self, root, screenshot):
        self.root = root
        self.root.title("游戏截图")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.screenshot = screenshot
        self.photo = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.selection_rect = None
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.root.geometry(f"{self.screenshot.width}x{self.screenshot.height}")

        self.show_result_button = tk.Button(root, text="显示坐标", command=self.show_result)
        self.show_result_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.copy_to_clipboard_button = tk.Button(root, text="复制坐标到剪贴板（开发用）", command=self.copy_result_to_clipboard)
        self.copy_to_clipboard_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_screenshot_button = tk.Button(root, text="保存完整截图", command=self.save_screenshot)
        self.save_screenshot_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_selection_button = tk.Button(root, text="保存选取截图", command=self.save_selection)
        self.save_selection_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.ocr_selection_button = tk.Button(root, text="OCR识别选取区域", command=self.ocr_selection)
        self.ocr_selection_button.pack(side=tk.LEFT, padx=5, pady=5)

    def get_selection_info(self):
        end_x, end_y = self.canvas.coords(self.selection_rect)[2:4]
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)
        x = min(self.start_x, end_x)
        y = min(self.start_y, end_y)

        return width, height, x, y

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if not self.selection_rect:
            self.selection_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y,
                outline="red", width=3  # Set the width of the rectangle
            )

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        pass

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def show_result(self):
        if self.selection_rect:
            width, height, x, y = self.get_selection_info()
            result = f"Width: {width}, Height: {height}, X: {x}, Y: {y}"
            tk.messagebox.showinfo("结果", result)
        else:
            tk.messagebox.showinfo("结果", "还没有选择区域呢")

    def copy_result_to_clipboard(self):
        if self.selection_rect:
            width, height, x, y = self.get_selection_info()
            text = f"crop=({x} / {self.screenshot.width}, {y} / {self.screenshot.height}, {width} / {self.screenshot.width}, {height} / {self.screenshot.height})"
            self.copy_to_clipboard(text)
            result = f"{text}\n复制到剪贴板成功"
            tk.messagebox.showinfo("结果", result)
        else:
            tk.messagebox.showinfo("结果", "还没有选择区域呢")

    def save_screenshot(self):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        screenshot_path = os.path.abspath(r"screenshots\screenshot.png")
        self.screenshot.save(screenshot_path)
        os.startfile(os.path.dirname(screenshot_path))

    def save_selection(self):
        if self.selection_rect:
            width, height, x, y = self.get_selection_info()
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            screenshot_path = os.path.abspath(r"screenshots\selection.png")
            self.screenshot.crop((x, y, x + width, y + height)).save(screenshot_path)
            os.startfile(os.path.dirname(screenshot_path))
        else:
            tk.messagebox.showinfo("结果", "还没有选择区域呢")

    def ocr_selection(self):
        if self.selection_rect:
            width, height, x, y = self.get_selection_info()
            result = ocrClientMgr.mOcr.RecognizeMultiLines(self.screenshot.crop((x, y, x + width, y + height)))
            text = ""
            Flag = True
            for box in result:
                if Flag:
                    text = text + box[1][0]
                    Flag = False
                else:
                    text = text + "\n" + box[1][0]
            self.copy_to_clipboard(text)
            tk.messagebox.showinfo("结果", text + "\n\n复制到剪贴板成功")
        else:
            tk.messagebox.showinfo("结果", "还没有选择区域呢")

def ExitHandler():
    # 退出 OCR
    ocrClientMgr.mOcr.ExitOcr()

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
            title_ = "选择启动助手/或启动工具箱:"
            options_reg = dict()
            options_reg.update({"0:启动助手":0})
            options_reg.update({"1:启动工具箱":1})
            option_ = questionary.select(title_, list(options_reg.keys())).ask()
            value = options_reg.get(option_)
            if value == 0:
                appClient = AppClient()
                appClient.Main()
            elif value == 1:
                appTools = AppTools()
                appTools.Main()
                
        except KeyboardInterrupt:
            log.error(logMgr.Error("发生错误: 手动强制停止"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            log.error(logMgr.Error(f"发生错误: {e}"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)