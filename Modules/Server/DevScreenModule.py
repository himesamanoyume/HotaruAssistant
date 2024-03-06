import math,pyautogui,win32api,win32con,win32gui,time,threading,base64,requests,tkinter
# from Hotaru.Client.LogClientHotaru import logClientMgr
from tkinter import *


class DevScreenModule:
    def GetWindow(self, title):
        windows = pyautogui.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            return window
        return False

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
        
    def InitDevScreenLoop(self):
        self.window = self.GetWindow("崩坏：星穹铁道")

        if self.window:
            # 初始化
            def OnSize(evt):
                screenshot_pos = self.GetHonkaiWindowsInfo(self.window)
                window_x = screenshot_pos[0]
                window_y = screenshot_pos[1]
                window_width = screenshot_pos[2]
                window_height = screenshot_pos[3]
                
                TRANSCOLOUR = 'gray'
                tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
                tk.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
                tk.title('测试窗口')
                # tk.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
                tk.configure(width=evt.width,height=evt.height)
                canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)

            tk = tkinter.Tk()
            tk.attributes("-topmost", 1)

            TRANSCOLOUR = 'gray'
            tk.wm_attributes('-transparentcolor', TRANSCOLOUR)

            canvas = Canvas(tk)
            canvas.pack(fill=BOTH,expand=Y)
            
            tk.bind('<Configure>', OnSize)
            tk.mainloop()
            return True
        else:
            return False
        
    # def ShowText(self, text):
    #     for t in text:
    #         self.windowScreen.blit(t[0], t[1])

    def StartLoop(self):
        thread = threading.Thread(target=self.Loop)
        thread.start()

    def LoopTemp(self):
        print("111")

    def Loop(self):

        done = 0
        pygame_focus = False

        while not done:
            time.sleep(0.5)
            print("111")
            screenshotPos = self.GetHonkaiWindowsInfo(self.window)
            windowX = screenshotPos[0]
            windowY = screenshotPos[1]
            
            # win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, windowX, windowY, screenshotPos[2], screenshotPos[3], win32con.SWP_NOSIZE)

            # for event in pygame.event.get():
            #     # print(event)
            #     if event.type == pygame.WINDOWFOCUSGAINED:
            #         pygame_focus = True
            #     elif event.type == pygame.WINDOWFOCUSLOST:
            #         pygame_focus = False
            #     elif event.type == pygame.QUIT:
            #         done = 1
            #     elif event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_ESCAPE:
            #             done = 1
            #     elif event.type == pygame.WINDOWMOVED:
            #         windowX = event.x
            #         windowY = event.y
            #         # if window_x < 0:
            #         #     window_x = 0
            #         # if window_y < 0:
            #         #     window_y = 0
            #     # elif event.type == pygame.VIDEORESIZE:
            #     #     window_width, window_height = event.size

            # # 设置透明
            # self.windowScreen.fill((255, 0, 128))
            # # 显示文字
            # # self.ShowText()
            # pygame.display.update()