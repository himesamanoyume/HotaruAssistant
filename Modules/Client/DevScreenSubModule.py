import math,pyautogui,win32api,win32con,win32gui,time,threading,base64,requests,tkinter
from Hotaru.Client.LogClientHotaru import logMgr,log
from tkinter import *


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
        
    def InitDevScreenLoop(self, window):
        if not window is None:
            # 初始化
            def OnSize(evt):
                try:
                    screenshot_pos = self.GetHonkaiWindowsInfo(window)
                    window_x = screenshot_pos[0]
                    window_y = screenshot_pos[1]
                    window_width = screenshot_pos[2]
                    window_height = screenshot_pos[3]
                    
                    TRANSCOLOUR = 'gray'
                    tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
                    tk.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
                    tk.title('DevScreen')
                    # tk.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
                    tk.configure(width=evt.width,height=evt.height)
                    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
                except Exception:
                    tk.destroy()

            tk = tkinter.Tk()
            tk.attributes("-topmost", 1)

            TRANSCOLOUR = 'gray'
            tk.wm_attributes('-transparentcolor', TRANSCOLOUR)

            canvas = Canvas(tk)
            canvas.pack(fill=BOTH,expand=Y)
            
            tk.bind('<Configure>', OnSize)
            tk.mainloop()
        
            