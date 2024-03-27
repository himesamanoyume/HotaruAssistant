from States import *
import pyperclip

class CheckCdkeyState(BaseState):

    mStateName = 'CheckCdkeyState'

    def OnBegin(self):
        screenMgr.ChangeTo("cdkey")
        for cdkey in configMgr.mConfig[configMgr.mKey.CDKEY_LIST]:
            log.info(logMgr.Info("检测到有兑换码"))
            time.sleep(1)
            pyperclip.copy(cdkey)
            if screenMgr.ClickElement("./assets/images/screen/cdkey/cdkey_copy.png", "image", 0.9, maxRetries=5):
                time.sleep(0.5)
                if screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=5):
                    time.sleep(0.5)
                    if screenMgr.FindElement("./assets/images/screen/cdkey/cdkey_fast.png", "image", 0.9, maxRetries=5):
                        log.warning(logMgr.Warning(f"{cdkey},兑换过快,5秒后重试"))
                        time.sleep(5)
                        if screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=5):
                            time.sleep(0.5)
                            if screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=5):
                                log.info(logMgr.Info(f"{cdkey},兑换成功"))
                                time.sleep(1)
                                screenMgr.ChangeTo("cdkey")
                                continue
                    elif screenMgr.FindElement("./assets/images/screen/cdkey/cdkey_repeat.png", "image", 0.9, maxRetries=5):
                        log.warning(logMgr.Warning(f"{cdkey},已被兑换过了"))
                        time.sleep(1)
                        if screenMgr.ClickElement("./assets/images/screen/cdkey/cdkey_clear.png", "image", 0.9, maxRetries=5):
                            continue
                    elif screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=5):
                        log.info(logMgr.Info(f"{cdkey},兑换成功"))
                        time.sleep(1)
                        screenMgr.ChangeTo("cdkey")
                        continue
                        
        screenMgr.ChangeTo("menu")

    def OnRunning(self):
        return False

    def OnExit(self):
        return False