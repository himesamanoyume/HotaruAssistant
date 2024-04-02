from States import *

class CheckStoreState(BaseState):

    mStateName = 'CheckStoreState'

    def OnBegin(self):
        self.ExpressSupplyPass()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    def ExpressSupplyPass(self):
        screenMgr.ChangeTo('menu')
        if screenMgr.ClickElement("./assets/images/menu/store.png", "image", 0.9, maxRetries=3):
            temp = screenMgr.GetSingleLineText(crop=(511.0 / 1920, 885.0 / 1080, 398.0 / 1920, 51.0 / 1080), maxRetries=3)
            if not temp == None:
                remainingText = temp.split('：')[1]
                dataMgr.passRemaining = remainingText
            else:
                log.info(logMgr.Info("没有购买月卡"))
        else:
            log.warning(logMgr.Warning("无法检测月卡剩余天数"))
            return True