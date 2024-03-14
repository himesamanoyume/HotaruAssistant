import pyautogui,tkinter,os,time
from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.ConfigClientHotaru import configMgr
from tkinter import *
from Modules.Utils.GameWindow import GameWindow

class DetectDevScreenSubModule:

    def ShowDetectArea(self, detectArea):
        self.canvas.create_rectangle(
            detectArea[0]+3, detectArea[1]+3, detectArea[2]+3, detectArea[3]+3, outline="red", width=3
        )
        
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
        
            