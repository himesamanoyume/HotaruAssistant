import pyautogui,tkinter,os
from Hotaru.Client.LogClientHotaru import logMgr,log
from tkinter import *
from Modules.Utils.GameWindow import GameWindow


class DevScreenSubModule:

    def IsApplicationFullscreen(self, window):
        screenWidth, screenHeight = pyautogui.size()
        return (window.width, window.height) == (screenWidth, screenHeight)

    def GetWindowRegion(self, window):
        # 边框
        otherBorder = (window.width - 1920) // 2
        upBorder = window.height - 1080 - otherBorder

        if self.IsApplicationFullscreen(window):
            return (window.left, window.top, window.width, window.height)
        else:
            return (window.left, window.top - upBorder, window.width -
                    otherBorder - otherBorder, window.height)
    
    def GetHonkaiWindowsInfo(self, window, crop=(0, 0, 0, 0)):
        if crop == (0, 0, 0, 0):
            screenshotPos = self.GetWindowRegion(window)
            return screenshotPos
        else:
            left, top, width, height = self.GetWindowRegion(window)
            screenshotPos = int(left + width * crop[0]), int(top + height * crop[1]), int(width * crop[2]), int(height * crop[3])
            return screenshotPos
        

    def TakeScreenshot(self, title, crop=(0, 0, 0, 0)):
        window = GameWindow.GetWindow(title)
        if window:
            if crop == (0, 0, 0, 0):
                screenshot_pos = self.GetWindowRegion(window)
            else:
                left, top, width, height = self.GetWindowRegion(window)
                screenshot_pos = int(left + width * crop[0]), int(top + height * crop[1]), int(width * crop[2]), int(height * crop[3])

            screenshot = pyautogui.screenshot(region=screenshot_pos)
            return screenshot, screenshot_pos

        return False
        
    def ShowInputArea(self, inputArea):
        pass

    def OnButtonPress(self, event):
        print("OnButtonPress")
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if not self.selection_rect:
            self.selection_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y,
                outline="red", width=3  # Set the width of the rectangle
            )

    def OnMouseDrag(self, event):
        print("OnMouseDrag")
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, cur_x, cur_y)

    def OnButtonRelease(self, event):
        print("OnButtonRelease")
        pass
    
    def GetSelectionInfo(self):
        end_x, end_y = self.canvas.coords(self.selection_rect)[2:4]
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)
        x = min(self.start_x, end_x)
        y = min(self.start_y, end_y)

        return width, height, x, y
    
    def CopyToClipboard(self, text):
        self.tk.clipboard_clear()
        self.tk.clipboard_append(text)
        self.tk.update()

    def ShowResult(self):
        if self.selection_rect:
            width, height, x, y = self.GetSelectionInfo()
            result = f"Width: {width}, Height: {height}, X: {x}, Y: {y}"
            tkinter.messagebox.showinfo("结果", result)
        else:
            tkinter.messagebox.showinfo("结果", "还没有选择区域呢")

    # def CopyResultToClipboard(self):
    #     if self.selection_rect:
    #         width, height, x, y = self.GetSelectionInfo()
    #         text = f"crop=({x} / {self.screenshot.width}, {y} / {self.screenshot.height}, {width} / {self.screenshot.width}, {height} / {self.screenshot.height})"
    #         self.CopyToClipboard(text)
    #         result = f"{text}\n复制到剪贴板成功"
    #         tkinter.messagebox.showinfo("结果", result)
    #     else:
    #         tkinter.messagebox.showinfo("结果", "还没有选择区域呢")

    # def SaveScreenshot(self):
    #     if not os.path.exists("screenshots"):
    #         os.makedirs("screenshots")
    #     screenshot_path = os.path.abspath(r"screenshots\screenshot.png")
    #     self.screenshot.save(screenshot_path)
    #     os.startfile(os.path.dirname(screenshot_path))

    # def SaveSelection(self):
    #     if self.selection_rect:
    #         width, height, x, y = self.GetSelectionInfo()
    #         if not os.path.exists("screenshots"):
    #             os.makedirs("screenshots")
    #         screenshotPath = os.path.abspath(r"screenshots\selection.png")
    #         self.screenshot.crop((x, y, x + width, y + height)).save(screenshotPath)
    #         os.startfile(os.path.dirname(screenshotPath))
    #     else:
    #         tkinter.messagebox.showinfo("结果", "还没有选择区域呢")
        
    def InitDevScreenLoop(self, window):
        if not window is None:
            # 初始化
            def OnSize(evt):
                try:

                    screenshotPos = self.GetHonkaiWindowsInfo(window)
                    window_x = screenshotPos[0]
                    window_y = screenshotPos[1]
                    window_width = screenshotPos[2]
                    window_height = screenshotPos[3]
                    
                    TRANSCOLOUR = 'gray'
                    self.tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
                    self.tk.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
                    self.tk.title('DevScreen')

                    self.tk.configure(width=evt.width,height=evt.height)
                    self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
                    self.canvas.create_rectangle(0, 0, self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, outline="red", width=3)

                except Exception:
                    log.error(logMgr.Error("窗口将自动关闭"))
                    self.tk.destroy()

            self.tk = tkinter.Tk()
            self.tk.attributes("-topmost", 1)

            TRANSCOLOUR = 'gray'
            self.tk.wm_attributes('-transparentcolor', TRANSCOLOUR)

            self.canvas = Canvas(self.tk)

            self.canvas.bind("<ButtonPress-1>", self.OnButtonPress)
            self.canvas.bind("<B1-Motion>", self.OnMouseDrag)
            self.canvas.bind("<ButtonRelease-1>", self.OnButtonRelease)

            self.TakeScreenshotButton = tkinter.Button(self.tk, text="截图", command=self.TakeScreenshot)
            self.TakeScreenshotButton.pack(side=tkinter.LEFT, padx=5, pady=5)
            self.ShowResultButton = tkinter.Button(self.tk, text="显示坐标", command=self.ShowResult)
            self.ShowResultButton.pack(side=tkinter.LEFT, padx=5, pady=5)

            self.canvas.pack(fill=BOTH,expand=Y)
            
            self.tk.bind('<Configure>', OnSize)
            

            

            self.tk.mainloop()
        
            