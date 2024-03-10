import pyautogui,tkinter,os,time
from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.ConfigClientHotaru import configMgr
from tkinter import *
from Modules.Utils.GameWindow import GameWindow

class DetectDevScreenSubModule:

    def ShowDetectArea(self, detectArea):
        self.canvas.create_rectangle(
            detectArea[0], detectArea[1], detectArea[2], detectArea[3], outline="red", width=3
        )

    # def OnButtonPress(self, event):
    #     print("OnButtonPress")
    #     self.start_x = self.canvas.canvasx(event.x)
    #     self.start_y = self.canvas.canvasy(event.y)

    #     if not self.selection_rect:
    #         self.selection_rect = self.canvas.create_rectangle(
    #             self.start_x, self.start_y, self.start_x, self.start_y,
    #             outline="red", width=3  # Set the width of the rectangle
    #         )

    # def OnMouseDrag(self, event):
    #     print("OnMouseDrag")
    #     cur_x = self.canvas.canvasx(event.x)
    #     cur_y = self.canvas.canvasy(event.y)

    #     self.canvas.coords(self.selection_rect, self.start_x, self.start_y, cur_x, cur_y)

    # def OnButtonRelease(self, event):
    #     print("OnButtonRelease")
    #     pass
    
    # def GetSelectionInfo(self):
    #     end_x, end_y = self.canvas.coords(self.selection_rect)[2:4]
    #     width = abs(end_x - self.start_x)
    #     height = abs(end_y - self.start_y)
    #     x = min(self.start_x, end_x)
    #     y = min(self.start_y, end_y)

        # return width, height, x, y
    
    # def CopyToClipboard(self, text):
    #     self.tk.clipboard_clear()
    #     self.tk.clipboard_append(text)
    #     self.tk.update()

    # def ShowResult(self):
    #     if self.selection_rect:
    #         width, height, x, y = self.GetSelectionInfo()
    #         result = f"Width: {width}, Height: {height}, X: {x}, Y: {y}"
    #         tkinter.messagebox.showinfo("结果", result)
    #     else:
    #         tkinter.messagebox.showinfo("结果", "还没有选择区域呢")

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
    #     screenshotPath = os.path.abspath(r"screenshots\screenshot.png")
    #     self.screenshot.save(screenshotPath)
    #     os.startfile(os.path.dirname(screenshotPath))

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
                    time.sleep(0.01)
                    screenshotPos = GameWindow.GetHonkaiWindowsInfo(window)
                    window_x = screenshotPos[0]
                    window_y = screenshotPos[1]
                    window_width = screenshotPos[2]
                    window_height = screenshotPos[3]
                    self.tk.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
                    

                except Exception as e:
                    log.error(logMgr.Error(f"窗口将自动关闭:{e}"))
                    self.tk.destroy()

            self.tk = tkinter.Tk()
            self.tk.attributes("-topmost", 1)
            self.tk.title('DevScreen')
            self.isScreenshot = False
            self.selectionRect = None

            TRANSCOLOUR = 'gray'
            self.tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
            self.canvas = Canvas(self.tk)
            self.canvas.configure(bg=TRANSCOLOUR)
            self.canvas.pack(fill=BOTH,expand=Y)
            self.tk.bind('<Configure>', OnSize)
            self.tk.mainloop()
        
            