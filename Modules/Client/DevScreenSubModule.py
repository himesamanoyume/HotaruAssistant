import math,pyautogui,pygame,pygame,win32api,win32con,win32gui,time,threading,base64,requests
from Hotaru.Client.LogClientHotaru import logClientMgr


class DevScreenSubModule:
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
        pygame.init()
        self.window = self.GetWindow("崩坏：星穹铁道")

        if self.window:
            # 初始化
            screenshotPos = self.GetHonkaiWindowsInfo(self.window)
            windowWidth = screenshotPos[2]
            windowHeight = screenshotPos[3]
            self.windowScreen = pygame.display.set_mode((windowWidth, windowHeight), pygame.SWSURFACE)
            pygame.display.set_caption("DevScreen")
            self.hwnd = pygame.display.get_wm_info()["window"]
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)
            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, screenshotPos[0], screenshotPos[1], screenshotPos[2], screenshotPos[3], win32con.SWP_NOSIZE)
            self.windowScreen.fill((255, 0, 128))

            # font = pygame.font.SysFont("Times New Roman", 54)
            # # 要展示的文本
            # text = []
            # # 设置文本位置
            # text.append((font.render("transparent window", 0, (255, 100, 0)), (20, 10)))
            # text.append((font.render("ESC to exit", 0, (255, 100, 100)), (20, 100)))
            logClientMgr.Info("DevScreen完成初始化")
            return True
        else:
            return False
        
    def ShowText(self, text):
        for t in text:
            self.windowScreen.blit(t[0], t[1])

    def StartLoop(self):
        thread = threading.Thread(target=self.Loop)
        thread.start()

    def LoopTemp(self):
        while True:
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