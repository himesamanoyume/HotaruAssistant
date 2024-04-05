from States.Client import *

class GetFAndPInfoState(BaseClientState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'GetFAndPState'

    def OnBegin(self):
        GetFAndPInfoState.GetForgottenHallInfo()
        GetFAndPInfoState.GetPureFictionInfo()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    @staticmethod
    def GetForgottenHallInfo():
        screenClientMgr.ChangeTo('guide4')
        # guide4_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        guide4LittleCrop=(250.0 / 1920, 413.0 / 1080, 432.0 / 1920, 488.0 / 1080)
        # little_crop指第一行不在范围内的坐标
        if screenClientMgr.ClickElement("忘却之庭", "text", maxRetries=20, crop=guide4LittleCrop):
            time.sleep(1)
            countdownTextCrop=(1484.0 / 1920, 556.0 / 1080, 135.0 / 1920, 27.0 / 1080)
            levelTextCrop=(1312.0 / 1920, 641.0 / 1080, 95.0 / 1920, 31.0 / 1080)
            starTextCrop=(1309.0 / 1920, 682.0 / 1080, 102.0 / 1920, 33.0 / 1080)
            try:
                time.sleep(0.5)
                countdownText = screenClientMgr.GetSingleLineText(crop=countdownTextCrop, blacklist=[], maxRetries=6)
                countdownText = countdownText.replace('）','').replace(')','').replace('①','').replace('?','')
                if countdownText == '?':
                    countdownText = '识别出错'
                levelText = screenClientMgr.GetSingleLineText(crop=levelTextCrop, blacklist=[], maxRetries=3)
                starText = screenClientMgr.GetSingleLineText(crop=starTextCrop, blacklist=[], maxRetries=3)
                log.info(logMgr.Info(f"忘却之庭刷新倒计时:{countdownText},层数:{levelText},星数:{starText}"))
                # Utils._content['fh_countdownText'] = countdownText
                dataClientMgr.notifyContent["混沌回忆倒计时"] = countdownText

                level = levelText.split('/')[0]
                star = starText.split('/')[0]
                configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataClientMgr.currentUid] = int(level)
                configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataClientMgr.currentUid] = int(star)
            except Exception as e:
                nowtime = time.time()
                log.error(logMgr.Error(f"{nowtime},识别忘却之庭失败:{e}"))
                raise Exception(f"{nowtime},识别忘却之庭失败:{e}")

        return True
    
    @staticmethod
    def GetPureFictionInfo():
        screenClientMgr.ChangeTo('guide4')
        # guide4_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        guide4LittleCrop=(250.0 / 1920, 413.0 / 1080, 432.0 / 1920, 488.0 / 1080)
        # little_crop指第一行不在范围内的坐标
        if screenClientMgr.ClickElement("虚构叙事", "text", maxRetries=20, crop=guide4LittleCrop):
            time.sleep(1)
            countdownTextCrop=(1484.0 / 1920, 556.0 / 1080, 135.0 / 1920, 27.0 / 1080)
            levelTextCrop=(1312.0 / 1920, 641.0 / 1080, 95.0 / 1920, 31.0 / 1080)
            starTextCrop=(1309.0 / 1920, 682.0 / 1080, 102.0 / 1920, 33.0 / 1080)
            try:
                time.sleep(0.5)
                countdownText = screenClientMgr.GetSingleLineText(crop=countdownTextCrop, blacklist=[], maxRetries=6)
                countdownText = countdownText.replace('）','').replace(')','').replace('①','').replace('?','')
                if countdownText == '?':
                    countdownText = '识别出错'
                levelText = screenClientMgr.GetSingleLineText(crop=levelTextCrop, blacklist=[], maxRetries=3)
                starText = screenClientMgr.GetSingleLineText(crop=starTextCrop, blacklist=[], maxRetries=3)
                log.info(logMgr.Info(f"虚构叙事刷新倒计时:{countdownText},层数:{levelText},星数:{starText}"))
                # Utils._content['pf_countdownText'] = countdownText

                dataClientMgr.notifyContent["虚构叙事倒计时"] = countdownText
                level = levelText.split('/')[0]
                star = starText.split('/')[0]
                configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataClientMgr.currentUid] = int(level)
                configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataClientMgr.currentUid] = int(star)
            except Exception as e:
                nowtime = time.time()
                log.error(logMgr.Error(f"{nowtime},识别虚构叙事失败:{e}"))
                raise Exception(f"{nowtime},识别虚构叙事失败:{e}")

        return True