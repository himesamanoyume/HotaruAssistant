from managers.logger_manager import logger
from managers.automation_manager import auto
from managers.screen_manager import screen
import sys,pyuac,os,questionary,time,pyautogui
from module.config.config import Config
from managers.translate_manager import _

class Reg:
    def main():
        logger.warning("在进行选择前,需要先手动把游戏退出!!!然后检查config.yaml中的game_path是否正确填入")
        title_ = "若已经关闭游戏,用方向键然后回车键选择你要做的:"
        options_reg = dict()
        options_reg.update({"0:选择获取新的注册表(会重新启动游戏,因此需要提前关闭游戏)":0})
        options_reg.update({"1:选择重新导入完整注册表(导入注册表后需要重启游戏才会生效)":1})
        options_reg.update({"2:进行截图":2})
        option_ = questionary.select(title_, list(options_reg.keys())).ask()
        value = options_reg.get(option_)
        if value == 0:
            Reg.reg_export()
        elif value == 1:
            Reg.restore_reg()
        elif value == 2:
            Reg.take_ss_first()
    
    def take_ss_first():
        Reg.take_screenshot()
        Reg.take_ss_second()

    def take_ss_second():
        options_reg2 = dict()
        options_reg2.update({"0:继续截图":0})
        options_reg2.update({"1:退出":1})
        option_ = questionary.select("截图已完成,选择下一步", list(options_reg2.keys())).ask()
        value = options_reg2.get(option_)
        if value == 0:
            Reg.take_ss_first()
        else:
            pass


    def restore_reg():
        logger.info("重新导入完整注册表")
        config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
        os.system(f"cmd /C reg import ./reg/temp-full.reg")

    def take_screenshot():
        from tasks.base.windowswitcher import WindowSwitcher
        from module.automation.screenshot import Screenshot
        config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
        if WindowSwitcher.check_and_switch(config.game_title_name):
            result = Screenshot.take_screenshot(config.game_title_name)
            if result:
                root = tk.Tk()
                app = ScreenshotApp(root, result[0])
                root.mainloop()

    def reg_export():
        from tasks.game.start import Start
        from tasks.base.windowswitcher import WindowSwitcher
        try:
            config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
            # 保存完整的注册表
            logger.info("保存完整的注册表")
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 ./reg/temp-full.reg /y")
            # 删除所有注册表
            logger.info("删除所有注册表")
            os.system(f"cmd /C reg delete HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 /f")
            # 等待游戏启动并登录
            logger.info("等待游戏启动并登录,登录完账号后,在可点击【进入游戏】界面等待脚本画面识别")
            logger.info("待脚本自动点击【进入游戏】之后等待加载至主界面,同时确保分辨率已调整至1920*1080全屏幕...")
            # os.system(f"cmd /C start \"\" \"{config.game_path}\"")
            
            Start.start_game()
            time.sleep(1)
            pyautogui.hotkey('alt', 'tab')
            
            input("是否已完成加载到主界面?若完成则按回车进入下一步开始识别UID...")

            # Resolution.check(config.game_title_name, 1920, 1080)
            WindowSwitcher.check_and_switch(config.game_title_name)
            logger.info("正在自动识别UID")

            screen.change_to("main")

            uid = auto.get_single_line_text(crop = (70.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080), blacklist=[], max_retries=9)

            time.sleep(1)
            pyautogui.hotkey('alt', 'tab')

            options_reg2 = dict()
            options_reg2.update({f"正确,直接导出":0})
            options_reg2.update({"错误,手动输入UID":1})
            option_ = questionary.select(f"识别UID:{uid},是否正确?根据情况选择下列选项:", list(options_reg2.keys())).ask()
            value = options_reg2.get(option_)
            if value == 0:
                pass
            elif value == 1:
                uid = input("手动输入UID:\n")
            # end
            # 导出对应账号注册表
            logger.info("导出对应账号注册表")
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 ./reg/starrail-{uid}.reg /y")
            # 重新导入完整注册表
            logger.info("重新导入完整注册表")
            os.system(f"cmd /C reg import ./reg/temp-full.reg")
            logger.info("完成,你已可以退出游戏,若要激活账号,需要到WEB后台的注册界面进行")

        except Exception as e:
            logger.error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(1)

import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os

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
            from managers.ocr_manager import ocr
            result = ocr.recognize_multi_lines(self.screenshot.crop((x, y, x + width, y + height)))
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

if __name__ == '__main__':

    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logger.error(_("管理员权限获取失败"))
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
    else:
        try:
            if not os.path.exists("./reg"):
                os.mkdir("./reg")
            Reg.main()
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error("发生错误: 手动强制停止")
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
        except Exception as e:
            logger.error(f"发生错误: {e}")
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)

