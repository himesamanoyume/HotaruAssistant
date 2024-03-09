from Hotaru.Client.LogClientHotaru import log,logMgr
import pyautogui,win32gui,time

class GameWindow:
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