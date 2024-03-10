from Hotaru.Client.LogClientHotaru import log,logMgr
import pyautogui,time

class ClickModule:

    pyautogui.FAILSAFE = False

    @staticmethod
    def MouseClick(x, y):
        try:
            pyautogui.click(x, y)
            log.debug(logMgr.Debug("鼠标点击 ({x}, {y})").format(x=x, y=y))
        except Exception as e:
            log.error(logMgr.Error("鼠标点击出错：{e}").format(e=e))

    @staticmethod
    def MouseDown(x, y):
        try:
            pyautogui.mouseDown(x, y)
            log.debug(logMgr.Debug("鼠标按下 ({x}, {y})").format(x=x, y=y))
        except Exception as e:
            log.error(logMgr.Error("鼠标按下出错：{e}").format(e=e))

    @staticmethod
    def MouseUp():
        try:
            pyautogui.mouseUp()
            log.debug(logMgr.Debug("鼠标释放"))
        except Exception as e:
            log.error(logMgr.Error("鼠标释放出错：{e}").format(e=e))

    @staticmethod
    def MouseMove(x, y):
        try:
            pyautogui.moveTo(x, y)
            log.debug(logMgr.Debug("鼠标移动 ({x}, {y})").format(x=x, y=y))
        except Exception as e:
            log.error(logMgr.Error("鼠标移动出错：{e}").format(e=e))

    @staticmethod
    def MouseScroll(count, direction=-1):
        for i in range(count):
            pyautogui.scroll(direction)
        log.debug(logMgr.Debug("滚轮滚动 {x} 次").format(x=count * direction))

    @staticmethod
    def PressKey(key, wait_time=0.2):
        try:
            pyautogui.keyDown(key)
            time.sleep(wait_time)
            pyautogui.keyUp(key)
            log.debug(logMgr.Debug("键盘按下 {key}").format(key=key))
        except Exception as e:
            log.debug(logMgr.Debug("键盘按下 {key} 出错：{e}").format(key=key, e=e))

    @staticmethod
    def PressMouse(wait_time=0.2):
        try:
            pyautogui.mouseDown()
            time.sleep(wait_time)
            pyautogui.mouseUp()
            log.debug(logMgr.Debug("按下鼠标左键"))
        except Exception as e:
            log.debug(logMgr.Debug("按下鼠标左键出错：{e}").format(e=e))
    
    