from Hotaru.Client.LogClientHotaru import log,logMgr
import pyautogui,time

class ClickScreenSubModule:

    pyautogui.FAILSAFE = False

    @staticmethod
    def MouseClick(x, y):
        try:
            pyautogui.click(x, y)
            log.debug(logMgr.Debug(f"鼠标点击 ({x}, {y})"))
        except Exception as e:
            log.error(logMgr.Error(f"鼠标点击出错：{e}"))

    @staticmethod
    def MouseDown(x, y):
        try:
            pyautogui.mouseDown(x, y)
            log.debug(logMgr.Debug(f"鼠标按下 ({x}, {y})"))
        except Exception as e:
            log.error(logMgr.Error(f"鼠标按下出错：{e}"))

    @staticmethod
    def MouseUp():
        try:
            pyautogui.mouseUp()
            log.debug(logMgr.Debug("鼠标释放"))
        except Exception as e:
            log.error(logMgr.Error(f"鼠标释放出错：{e}"))

    @staticmethod
    def MouseMove(x, y):
        try:
            pyautogui.moveTo(x, y)
            log.debug(logMgr.Debug(f"鼠标移动 ({x}, {y})"))
        except Exception as e:
            log.error(logMgr.Error(f"鼠标移动出错：{e}"))

    @staticmethod
    def MouseScroll(count, direction=-1):
        for i in range(count):
            pyautogui.scroll(direction)
        log.debug(logMgr.Debug(f"滚轮滚动 {count * direction} 次"))

    @staticmethod
    def PressKey(key, wait_time=0.2):
        try:
            pyautogui.keyDown(key)
            time.sleep(wait_time)
            pyautogui.keyUp(key)
            log.debug(logMgr.Debug(f"键盘按下 {key}"))
        except Exception as e:
            log.error(logMgr.Error(f"键盘按下 {key} 出错：{e}"))

    @staticmethod
    def PressMouse(wait_time=0.2):
        try:
            pyautogui.mouseDown()
            time.sleep(wait_time)
            pyautogui.mouseUp()
            log.debug(logMgr.Debug("按下鼠标左键"))
        except Exception as e:
            log.error(logMgr.Error(f"按下鼠标左键出错：{e}"))
    
    