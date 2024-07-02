from States.Client import *

class GetFAndPInfoState(BaseClientState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'GetFAndPInfoState'

    def OnBegin(self):
        GetFAndPInfoState.GetFPInfo() # "虚构叙事" || "忘却之庭" || "末日幻影"
        GetFAndPInfoState.GetFPInfo("虚构叙事")
        GetFAndPInfoState.GetFPInfo("末日幻影")

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    @staticmethod
    def GetFPInfo(typeStr:str = "忘却之庭"):
        screenClientMgr.ChangeTo('guide4')
        guide4LittleCrop=(250.0 / 1920, 413.0 / 1080, 432.0 / 1920, 488.0 / 1080)
        if screenClientMgr.ClickElement(typeStr, "text", maxRetries=3, crop=guide4LittleCrop):
            time.sleep(1)
            if typeStr == "忘却之庭":
                typeStr = "混沌回忆"
            instanceTypeCrop=(920.0 / 1920, 327.0 / 1080, 155.0 / 1920, 58.0 / 1080)
            screenClientMgr.ClickElement(typeStr, "text", maxRetries=3, crop=instanceTypeCrop)
            time.sleep(0.3)
            screenClientMgr.MouseScroll(2, -1)
            time.sleep(1)
            
            area1CountdownCrop=(1482.0 / 1920, 489.0 / 1080, 142.0 / 1920, 103.0 / 1080)
            area2CountdownCrop=(1480.0 / 1920, 723.0 / 1080, 145.0 / 1920, 42.0 / 1080)
            area1LevelStarCrop=(1320.0 / 1920, 460.0 / 1080, 93.0 / 1920, 293.0 / 1080)
            area2LevelStarCrop=(1320.0 / 1920, 693.0 / 1080, 97.0 / 1920, 233.0 / 1080)

            cropList = [(area1CountdownCrop, area1LevelStarCrop)]

            turn = 1

            if screenClientMgr.FindElement("./assets/static/images/screen/guide/check_detail.png", "image", 0.9, maxRetries=1, crop=(693.0 / 1920, 656.0 / 1080, 965.0 / 1920, 287.0 / 1080)):
                turn = 2
                cropList.append((area2CountdownCrop, area2LevelStarCrop))
            
            for i in range(turn):
                try:
                    time.sleep(1)

                    countdownText = screenClientMgr.GetSingleLineText(crop=cropList[i][0], blacklist=[], maxRetries=1)

                    countdownText = countdownText.replace('）','').replace(')','').replace('①','').replace('?','')

                    if countdownText == '?':
                        countdownText = '识别出错'

                    screenClientMgr.TakeScreenshot(crop=cropList[i][1])
                    result = ocrClientMgr.mOcr.RecognizeMultiLines(screenClientMgr.mDetect.screenshot)
                    if not result:
                        log.error(logMgr.Error("未检测到任何文字"))
                        return
                    
                    levelText = result[0][1][0]
                    starText = result[1][1][0]

                    log.info(logMgr.Info(f"{typeStr}{i + 1}刷新倒计时:{countdownText},层数:{levelText},星数:{starText}"))

                    # Utils._content['fh_countdownText'] = countdownText
                    dataClientMgr.notifyContent[f"{typeStr}{i + 1}倒计时"] = countdownText

                    level = levelText.split('/')[0]
                    star = starText.split('/')[0]
                    dataClientMgr.notifyContent[f"{typeStr}{i + 1}层数"] = int(level)
                    dataClientMgr.notifyContent[f"{typeStr}{i + 1}星数"] = int(star)

                except Exception as e:
                    nowtime = time.time()
                    log.error(logMgr.Error(f"{nowtime},识别{typeStr}{i + 1}失败:{e}"))
                    raise Exception(f"{nowtime},识别{typeStr}{i + 1}失败:{e}")

            levelList = [dataClientMgr.notifyContent[f"{typeStr}1层数"], dataClientMgr.notifyContent[f"{typeStr}2层数"]]
            starList = [dataClientMgr.notifyContent[f"{typeStr}1星数"], dataClientMgr.notifyContent[f"{typeStr}2星数"]]

            if typeStr == "混沌回忆":
                configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataClientMgr.currentUid] = levelList
                configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataClientMgr.currentUid] = starList
            elif typeStr == "末日幻影":
                configMgr.mConfig[configMgr.mKey.APOCALYPTICSHADOW_LEVELS][dataClientMgr.currentUid] = levelList
                configMgr.mConfig[configMgr.mKey.APOCALYPTICSHADOW_STARS][dataClientMgr.currentUid] = starList
            else:
                configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataClientMgr.currentUid] = levelList
                configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataClientMgr.currentUid] = starList
