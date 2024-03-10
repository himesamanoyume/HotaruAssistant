from Hotaru.Client.LogClientHotaru import log,logMgr
from Hotaru.Client.ConfigClientHotaru import configMgr
import pyautogui,win32gui,time

class GameWindow:

    @staticmethod
    def IsApplicationFullscreen(window):
        screenWidth, screenHeight = pyautogui.size()
        return (window.width, window.height) == (screenWidth, screenHeight)
    
    @staticmethod
    def GetWindowRegion(window):
        # 边框
        otherBorder = (window.width - 1920) // 2
        upBorder = window.height - 1080 - otherBorder

        if GameWindow.IsApplicationFullscreen(window):
            return (window.left, window.top, window.width, window.height)
        else:
            return (window.left + otherBorder, window.top + upBorder, window.width -
                    otherBorder - otherBorder, window.height - upBorder - otherBorder)

    @staticmethod
    def GetWindowDevRegion(window):
        # 边框
        otherBorder = (window.width - 1920) // 2
        upBorder = window.height - 1080 - otherBorder

        if GameWindow.IsApplicationFullscreen(window):
            return (window.left, window.top, window.width, window.height)
        else:
            return (window.left, window.top - upBorder, window.width -
                    otherBorder - otherBorder, window.height)
    
    @staticmethod
    def GetHonkaiWindowsInfo(window, crop=(0, 0, 0, 0)):
        if crop == (0, 0, 0, 0):
            screenshotPos = GameWindow.GetWindowDevRegion(window)
            return screenshotPos
        else:
            left, top, width, height = GameWindow.GetWindowDevRegion(window)
            screenshotPos = int(left + width * crop[0]), int(top + height * crop[1]), int(width * crop[2]), int(height * crop[3])
            return screenshotPos
        
    @staticmethod
    def TakeScreenshot(crop=(0, 0, 0, 0)):
        title = configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME]
        window = GameWindow.GetWindow(title)
        if window:
            if crop == (0, 0, 0, 0):
                screenshotPos = GameWindow.GetWindowRegion(window)
            else:
                left, top, width, height = GameWindow.GetWindowRegion(window)
                screenshotPos = int(left + width * crop[0]), int(top + height * crop[1]), int(width * crop[2]), int(height * crop[3])

            GameWindow.SwitchToWindow(title, maxRetries=4)
            screenshot = pyautogui.screenshot(region=screenshotPos)
            return screenshot, screenshotPos
        return False

    @staticmethod
    def GetWindow(title):
        windows = pyautogui.getWindowsWithTitle(title)
        if not windows:
            return False
        for window in windows:
            if window.title == title:
                return window
            
    @staticmethod
    def SwitchToWindow(title, maxRetries, isGameWindow = True):
        for i in range(maxRetries):
            window = GameWindow.GetWindow(title)
            if isGameWindow:
                try:
                    hwnd = win32gui.FindWindow("UnityWndClass", title)
                    win32gui.GetWindowRect(hwnd)
                except Exception as e:
                    continue
            try:
                window.restore()
                window.activate()
            except Exception as e:
                log.warning(logMgr.Warning(e))
            time.sleep(2)
            if window.isActive:
                if isGameWindow:
                    try:
                        hwnd = win32gui.FindWindow("UnityWndClass", title)
                        win32gui.GetWindowRect(hwnd)
                        return True
                    except Exception as e:
                        log.warning(logMgr.Warning(e))
            log.warning(logMgr.Warning("切换窗口失败,尝试ALT+TAB"))
            pyautogui.hotkey('alt', 'tab')
            time.sleep(2)
            continue
        return False