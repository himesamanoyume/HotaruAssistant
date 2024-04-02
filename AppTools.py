import sys,pyuac,os,questionary,pyautogui
from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.OcrHotaru import ocrMgr
from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.TaskHotaru import taskMgr
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import dataMgr

class AppTools:
    def main():
        dataMgr.gameTitleName = configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]
        log.hr(logMgr.Hr("在进行选择前,需要通读对应选项下的说明,若注册表修改操作不当可能导致游戏画面等设置全部被清空!!!本人概不负责", True))
        input("按回车进行下一步")
        log.hr(logMgr.Hr("1.如果需要获取注册表,则需要先手动把游戏、Client都退出!!!截图则不需要", True))
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
        if screenMgr.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]):
            result = screenMgr.TakeScreenshot()
            if result:
                root = tk.Tk()
                app = ScreenshotApp(root, screenMgr.mDetect.screenshot)
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
            log.hr(logMgr.Hr("3.启动游戏后,需要在10分钟内输入账号密码登录并进入游戏,否则判定为启动游戏失败", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("4.等待左下角显示UID后,切换到脚本窗口,按下回车识别UID,如果识别错误也可自行输入", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("5.然后你将获得对应UID账号的注册表文件(位于根目录./reg文件夹中,名称为starrail-xxxxxxxxx.reg)", True))
            input("按回车进行下一步")
            log.hr(logMgr.Hr("6.退出游戏,重新运行Regsiter,选择重新导入注册表,或直接双击temp-full.reg导入注册表,即可完成", True))
            input("若已阅读完毕,按回车开始获取注册表")
            # 保存完整的注册表
            log.info(logMgr.Info("正在保存完整的注册表"))
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 ./reg/temp-full.reg /y")
            # 删除所有注册表
            log.info(logMgr.Info("正在删除所有注册表"))
            os.system(f"cmd /C reg delete HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 /f")
            input("此刻已生成temp-full.reg文件,你可以选择在这个空档进行文件备份,或按回车正式开始启动游戏...")
            # 等待游戏启动并登录
            if taskMgr.StartGame():
                options_reg2 = dict()
                options_reg2.update({f"正确,直接导出":0})
                options_reg2.update({"错误,手动输入UID":1})
                option_ = questionary.select(f"识别UID:{dataMgr.currentUid},是否正确?根据情况选择下列选项:", list(options_reg2.keys())).ask()
                pyautogui.hotkey('alt', 'tab')
                value = options_reg2.get(option_)
                if value == 0:
                    uid = dataMgr.currentUid
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
            result = ocrMgr.mOcr.RecognizeMultiLines(self.screenshot.crop((x, y, x + width, y + height)))
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
    ocrMgr.mOcr.ExitOcr()

if __name__ == '__main__':

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
            if not os.path.exists("./reg"):
                os.mkdir("./reg")
            atexit.register(ExitHandler)
            AppTools.main()
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except KeyboardInterrupt:
            log.error(logMgr.Error("发生错误: 手动强制停止"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            log.error(logMgr.Error(f"发生错误: {e}"))
            input("按回车键关闭窗口. . .")
            sys.exit(0)

