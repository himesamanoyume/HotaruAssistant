import pyautogui,tkinter,os,time
from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.DataClientHotaru import dataMgr
from tkinter import *
from Modules.Utils.GameWindow import GameWindow

class DetectDevScreenSubModule:

    def __init__(self):
        self.isDevScreenRunning = False

    def ShowDetectArea(self, detectArea):
        temp0 = detectArea[0] * 1920
        temp1 = detectArea[1] * 1080
        temp2 = detectArea[2] * 1920
        temp3 = detectArea[3] * 1080
        detectArea = (temp2, temp3, temp0, temp1)

        window = GameWindow.GetWindow(dataMgr.gameTitleName)
        if window:
            upBorder = GameWindow.GetWindowDevBorder(window)
            
            log.debug(logMgr.Debug(f"正在显示检测区域: ({temp0}, {temp1}, {temp2}, {temp3})"))
            self.canvas.create_rectangle(
                detectArea[2] - 3, detectArea[3] + upBorder - 3, detectArea[2] + detectArea[0] + 3, detectArea[3] + detectArea[1] + upBorder + 3, outline="red", width=3
            )
        else:
            self.isDevScreenRunning = False
        
    def InitDevScreenLoop(self, window):
        if not window is None:
            # 初始化
            def OnSize(evt):
                try:
                    time.sleep(0.01)
                    screenshotPos = GameWindow.GetHonkaiWindowsInfo(window)
                    if not screenshotPos == False:
                        window_x = screenshotPos[0]
                        window_y = screenshotPos[1]
                        window_width = screenshotPos[2]
                        window_height = screenshotPos[3]
                        self.tk.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
                    else:
                        log.debug(logMgr.Debug(f"未检测到游戏窗口,DevScreen将自动关闭"))
                        self.isDevScreenRunning = False
                        self.tk.destroy() 
                        self.tk = None
                except Exception as e:
                    log.debug(logMgr.Debug(f"DevScreen将自动关闭:{e}"))
                    self.isDevScreenRunning = False
                    self.tk.destroy()    
                    self.tk = None

            self.tk = tkinter.Tk()
            self.tk.attributes("-topmost", 1)
            self.tk.title('Hotaru Assistant - SamDevScreen')
            self.isScreenshot = False
            self.selectionRect = None
            time.sleep(2)
            if GameWindow.IsApplicationFullscreen(window):
                log.debug(logMgr.Debug(f"DevScreen开启全屏模式"))
                self.tk.overrideredirect(True)

            TRANSCOLOUR = 'gray'
            self.tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
            self.canvas = Canvas(self.tk)
            self.canvas.configure(bg=TRANSCOLOUR)
            self.canvas.pack(fill=BOTH,expand=Y)
            self.tk.bind('<Configure>', OnSize)
            self.isDevScreenRunning = True
            self.tk.mainloop()   
            