from States.Client import *
import pyperclip

class CheckCdkeyState(BaseClientState):

    mStateName = 'CheckCdkeyState'

    def OnBegin(self):
        if not len(configMgr.mConfig[configMgr.mKey.CDKEY_LIST]) > 0:
            log.info(logMgr.Info("未检测到有兑换码"))
            return False
        screenClientMgr.ChangeTo("cdkey")
        for cdkey in configMgr.mConfig[configMgr.mKey.CDKEY_LIST]:
            log.info(logMgr.Info("检测到有兑换码"))
            pyperclip.copy(cdkey)
            if screenClientMgr.ClickElement("./assets/static/images/screen/cdkey/cdkey_copy.png", "image", 0.9):
                if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                    if screenClientMgr.FindElement("./assets/static/images/screen/cdkey/cdkey_fast.png", "image", 0.9):
                        log.warning(logMgr.Warning(f"{cdkey},兑换过快,5秒后重试"))
                        time.sleep(5)
                        if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                            if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                                log.info(logMgr.Info(f"{cdkey},兑换成功"))
                                screenClientMgr.ChangeTo("cdkey")
                                continue
                    elif screenClientMgr.FindElement("./assets/static/images/screen/cdkey/cdkey_repeat.png", "image", 0.9):
                        log.warning(logMgr.Warning(f"{cdkey},已被兑换过了"))
                        if screenClientMgr.ClickElement("./assets/static/images/screen/cdkey/cdkey_clear.png", "image", 0.9):
                            continue
                    elif screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                        log.info(logMgr.Info(f"{cdkey},兑换成功"))
                        screenClientMgr.ChangeTo("cdkey")
                        continue
                        
        screenClientMgr.ChangeTo("menu")

    def OnRunning(self):
        return False

    def OnExit(self):
        return False