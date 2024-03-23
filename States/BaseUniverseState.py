from States import *

class BaseUniverseState(BaseState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseUniverseState'

    @staticmethod
    def GetUniverseReward():
        screenMgr.ChangeTo("universe_main")
        time.sleep(2)
        # 如果一开始就能检测到积分奖励画面 说明是每周第一次进入界面刷新时
        if screenMgr.FindElement("./assets/images/screen/universe/universe_score.png", "image", 0.9, maxRetries=3):
            log.info(logMgr.Info("检测到模拟宇宙本周首次进入界面"))
            time.sleep(1)
            currentScore, maxScore = BaseUniverseState.GetUniverseScore()
            screenMgr.ClickElement("./assets/images/himeko/close.png", "image", 0.9, maxRetries=3)

        elif screenMgr.ClickElement("./assets/images/universe/universe_reward.png", "image", 0.9, maxRetries=3):
            log.info(logMgr.Info("正在点开积分界面"))
            time.sleep(1)
            currentScore, maxScore = BaseUniverseState.GetUniverseScore()
            if screenMgr.ClickElement("./assets/images/universe/one_key_receive.png", "image", 0.9, maxRetries=3):
                time.sleep(0.5)
                if screenMgr.FindElement("./assets/images/himeko/close.png", "image", 0.9, maxRetries=3):
                    time.sleep(0.5)
                    log.info(logMgr.Info("🎉模拟宇宙积分奖励已领取🎉"))
                    screenMgr.ClickElement("./assets/images/himeko/close.png", "image", 0.9, maxRetries=3)
        
        return currentScore, maxScore

    @staticmethod
    def GetUniverseScore():
        scoreCrop = (267.0 / 1920, 738.0 / 1080, 271.0 / 1920, 57.0 / 1080)
        time.sleep(1)
        try:
            scoreAndMaxScore = screenMgr.GetSingleLineText(crop=scoreCrop, blacklist=[], maxRetries=5)
            log.info(logMgr.Info(f"识别到文字为:{scoreAndMaxScore}"))
            configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][dataMgr.currentUid] = scoreAndMaxScore

            currentScore = scoreAndMaxScore.split('/')[0]
            maxScore = scoreAndMaxScore.split('/')[1]

            log.info(logMgr.Info(f"识别到当前积分为:{currentScore}"))
            log.info(logMgr.Info(f"识别到积分上限为:{maxScore}"))
            if int(currentScore) == int(maxScore):
                log.info(logMgr.Info(f"模拟宇宙积分已满"))
                configMgr.mConfig[configMgr.mKey.UNIVERSE_FIN][dataMgr.currentUid] = True
                dataMgr.isDetectUniverseScoreAndFinished = True
                configMgr.SaveTimestampByUid(configMgr.mKey.UNIVERSE_TIMESTAMP, dataMgr.currentUid)
            else:
                log.info(logMgr.Info(f"模拟宇宙积分未满"))
                configMgr.mConfig[configMgr.mKey.UNIVERSE_FIN][dataMgr.currentUid] = False
                
            return int(currentScore), int(maxScore)
        except Exception as e:
            log.error(logMgr.Error(f"识别模拟宇宙积分失败: {e}"))
            configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][dataMgr.currentUid] = '0/1'
            log.warning(logMgr.Warning("因读取模拟宇宙积分失败,程序中止"))

    @staticmethod
    def OpenUniverseScoreScreen():
        screenMgr.ChangeTo("universe_main")
        time.sleep(2)
        # 如果一开始就能检测到积分奖励画面 说明是每周第一次进入界面刷新时
        if screenMgr.FindElement("./assets/images/screen/universe/universe_score.png", "image", 0.9, maxRetries=10):
            log.info(logMgr.Info("检测到模拟宇宙本周首次进入界面"))
            time.sleep(1)
            currentScore, maxScore = BaseUniverseState.GetUniverseScore()
            screenMgr.ClickElement("./assets/images/himeko/close.png", "image", 0.9, maxRetries=10)

        elif screenMgr.ClickElement("./assets/images/universe/universe_reward.png", "image", 0.9, maxRetries=10):
            log.info(logMgr.Info("正在点开积分界面"))
            time.sleep(1)
            currentScore, maxScore = BaseUniverseState.GetUniverseScore()
            if screenMgr.FindElement("./assets/images/universe/one_key_receive.png", "image", 0.9, maxRetries=10):
                time.sleep(0.5)
                if screenMgr.FindElement("./assets/images/himeko/close.png", "image", 0.9, maxRetries=10):
                    time.sleep(0.5)
                    log.info(logMgr.Info("🎉模拟宇宙积分奖励已领取🎉"))
                    screenMgr.ClickElement("./assets/images/himeko/close.png", "image", 0.9, maxRetries=10)
        
        return currentScore, maxScore

    @staticmethod
    def GetImmersifier():
        screenMgr.ChangeTo('guide3')
        instanceTypeCrop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        if configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0] == '模拟宇宙':
            if dataMgr.currentPower >= 40:
                count = dataMgr.currentPower // 40
                log.info(logMgr.Info(f"开拓力能换{count}个沉浸器"))
                if screenMgr.ClickElement("./assets/images/share/trailblaze_power/immersifiers.png", "image", 0.95, maxRetries=10):
                    time.sleep(0.5)
                
                    for i in range(count-1):
                        screenMgr.ClickElement("./assets/images/share/trailblaze_power/plus.png", "image", 0.9, maxRetries=10)
                        time.sleep(0.5)

                    if screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=10):
                        time.sleep(1)
                        screenMgr.PressMouse()

        if not screenMgr.ClickElement("模拟宇宙", "text", crop=instanceTypeCrop):
            if screenMgr.ClickElement("凝滞虚影", "text", maxRetries=10, crop=instanceTypeCrop):
                screenMgr.MouseScroll(12, 1)
                screenMgr.ClickElement("模拟宇宙", "text", crop=instanceTypeCrop)

        time.sleep(0.5)
        try:
            result = screenMgr.GetSingleLineText(crop=(1673.0 / 1920, 50.0 / 1080, 71.0 / 1920, 31.0 / 1080),maxRetries=5)
            count = result.split("/")[0]
            log.info(logMgr.Info(f"识别到沉浸器数量为:{count}"))
            dataMgr.currentImmersifiers = int(count)
        except Exception as e:
            log.error(logMgr.Error(f"识别沉浸器数量失败: {e}"))
            dataMgr.currentImmersifiers = 0