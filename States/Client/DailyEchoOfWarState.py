from States.Client import *
import time
from .BaseFightState import BaseFightState

class DailyEchoOfWarState(BaseFightState, BaseClientState):

    mStateName = 'DailyEchoOfWarState'

    def OnBegin(self):
        log.hr(logMgr.Hr("进入历战余响部分"), 2)
        if configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_ENABLE][dataClientMgr.currentUid]:
            rewardCount = self.EchoOfWarGetTimes()
            if rewardCount > 0:
                self.EchoOfWarStart(rewardCount)
            else:
                if not Date.IsNextWeek4AM(configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_TIMESTAMP][dataClientMgr.currentUid], dataClientMgr.currentUid):
                    log.info(logMgr.Info("历战余响尚\033[91m未刷新\033[0m"))
                    return True
        else:
            log.info(logMgr.Info("历战余响\033[91m未开启\033[0m"))
            return True
        
        log.hr(logMgr.Hr("历战余响部分结束"), 2)

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    @staticmethod
    def EchoOfWarGetTimes():
        screenClientMgr.ChangeTo('guide3')
        guide3Crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        log.info(logMgr.Info(f"开始检测历战余响本周可领取奖励次数"))
        if screenClientMgr.ClickElement("侵蚀隧洞", "text", crop=guide3Crop):
            screenClientMgr.MouseScroll(12, -1)
            if screenClientMgr.ClickElement("历战余响", "text", crop=guide3Crop):
                screenClientMgr.FindElement("历战余响", "text", crop=(
                    682.0 / 1920, 275.0 / 1080, 1002.0 / 1920, 184.0 / 1080), include=True)
                for box in screenClientMgr.mDetect.ocrResult:
                    text = box[1][0]
                    if "/3" in text:
                        log.info(logMgr.Info(f"历战余响本周可领取奖励次数：{text}"))
                        rewardCount = int(text.split("/")[0])

                        configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_TIMES][dataClientMgr.currentUid] = rewardCount
                        return rewardCount
        else:
            return False
                    
    def EchoOfWarStart(self, rewardCount):
        try:
            log.hr(logMgr.Hr("准备历战余响"), 2)
            maxCount = dataClientMgr.currentPower // 30
            if maxCount == 0:
                log.info(logMgr.Info("🟣开拓力 < 30, 无法进行历战余响"))
                return
            elif rewardCount <= maxCount:
                configMgr.SaveTimestampByUid(configMgr.mKey.ECHO_OF_WAR_TIMESTAMP, dataClientMgr.currentUid)

            return self.RunInstances("历战余响", configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataClientMgr.currentUid]["历战余响"], 30, min(rewardCount, maxCount))
        except Exception as e:
            log.error(logMgr.Error(f"历战余响失败: {e}"))
            return False