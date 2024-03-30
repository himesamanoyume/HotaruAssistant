from States import *

class CheckStoreState(BaseState):

    mStateName = 'CheckStoreState'

    def OnBegin(self):
        self.ExpressSupplyPass()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    def ExpressSupplyPass():
        screenMgr.ChangeTo('menu')
        if screenMgr.ClickElement("./assets/images/menu/store.png", "image", 0.9, maxRetries=3):
            remainingText = screenMgr.GetSingleLineText(crop=(511.0 / 1920, 885.0 / 1080, 398.0 / 1920, 51.0 / 1080), maxRetries=3).split('：')[1]
            dataMgr.passRemaining = remainingText
        else:
            log.warning(logMgr.Error("无法检测月卡剩余天数"))
            return True