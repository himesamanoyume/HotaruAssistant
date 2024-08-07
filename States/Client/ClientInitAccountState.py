from States.Client import *

class ClientInitAccountState(BaseClientState):

    mStateName = 'ClientInitAccountState'

    def OnBegin(self):
        uidCrop = (70.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080)
        try:
            dataClientMgr.currentUid = screenClientMgr.GetSingleLineText(crop=uidCrop, blacklist=[])
            if dataClientMgr.currentUid == None:
                nowtime = time.time()
                log.error(logMgr.Error(f"未能读取到UID"))
                raise Exception(f"未能读取到UID")
            dataClientMgr.loopStartTimestamp = time.time()
            log.info(logMgr.Info(f"识别到UID为:{dataClientMgr.currentUid}"))
            configMgr.mConfig.SetValue(configMgr.mKey.LAST_RUNNING_UID, dataClientMgr.currentUid)
        except Exception as e:
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},识别UID失败: {e}"))
            raise Exception(f"{nowtime},识别UID失败: {e}")

    def OnRunning(self):
        if Date.IsNext4AM(configMgr.mConfig[configMgr.mKey.LAST_RUN_TIMESTAMP][dataClientMgr.currentUid]):
            log.info(logMgr.Info("已是新的一天,开始每日"))
            if len(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataClientMgr.currentUid]) == 1:
                pass
            else:
                if configMgr.mConfig[configMgr.mKey.LAST_RUN_TIMESTAMP][dataClientMgr.currentUid] == 0:
                    pass
                else:
                    configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataClientMgr.currentUid].remove(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataClientMgr.currentUid][0])

            screenClientMgr.ChangeTo('activity')
            activityList = []
            
            # 部分活动在选中情况下 OCR 识别困难
            screenClientMgr.ClickElement("锋芒斩露", "text", None, crop=(53.0 / 1920, 109.0 / 1080, 190.0 / 1920, 846.0 / 1080), include=True)

            screenClientMgr.TakeScreenshot(crop=(46.0 / 1920, 107.0 / 1080, 222.0 / 1920, 848.0 / 1080))

            result = ocrClientMgr.mOcr.RecognizeMultiLines(screenClientMgr.mDetect.screenshot)
            if not result:
                log.info(logMgr.Info("未检测到任何活动"))
                return

            for box in result:
                text = box[1][0]
                if len(text) >= 4:
                    activityList.append(text)

            if "巡星之礼" in activityList:
                self.GetReward("巡星之礼")
            if "巡光之礼" in activityList:
                self.GetReward("巡光之礼")

            screenClientMgr.ChangeTo("guide2")
            self.StartDetectDailyTasks()
            configMgr.mConfig.SetValue(configMgr.mKey.DAILY_TASKS, dataClientMgr.tempDailyTasksList)
            configMgr.SaveTimestampByUid(configMgr.mKey.LAST_RUN_TIMESTAMP, dataClientMgr.currentUid)
        else:
            log.info(logMgr.Info("日常任务\033[91m未刷新\033[0m"))

        self.CalcDailyTasksScore()


    def OnExit(self):
        return False
    
    @staticmethod
    def GetReward(targetText="巡星之礼"):
        screenClientMgr.ChangeTo('activity')
        
        if screenClientMgr.ClickElement(targetText, "text", None, crop=(46.0 / 1920, 107.0 / 1080, 222.0 / 1920, 848.0 /1080)):
            receive_path = "./assets/static/images/activity/giftof/receive.png"
            receive_fin_path = "./assets/static/images/activity/giftof/receive_fin.png"
            if screenClientMgr.FindElement(receive_path, "image", 0.9) or screenClientMgr.FindElement(receive_fin_path, "image", 0.9):
                log.hr(logMgr.Hr(f"检测到{targetText}奖励"), 2)
                while screenClientMgr.ClickElement(receive_path, "image", 0.9) or screenClientMgr.ClickElement(receive_fin_path, "image", 0.9):
                    screenClientMgr.ClickElement("./assets/static/images/base/click_close.png", "image", 0.9)
                log.info(logMgr.Info(f"领取{targetText}奖励完成"))
            else:
                log.warning(logMgr.Warning(f"未能领取{targetText}奖励"))
        else:
            log.warning(logMgr.Warning(f"未能领取{targetText}奖励"))

    def StartDetectDailyTasks(self):
        crop = (243.0 / 1920, 377.0 / 1080, 1428.0 / 1920, 528.0 / 1080)
        if configMgr.mConfig[configMgr.mKey.DAILY_TASKS] == {}:
            dataClientMgr.tempDailyTasksList = {}
        else:
            dataClientMgr.tempDailyTasksList = configMgr.mConfig[configMgr.mKey.DAILY_TASKS]

        self.DetectDailyTasks(crop)
        screenClientMgr.ClickElement("./assets/static/images/quest/activity.png", "image", 0.95, crop=crop)
        screenClientMgr.MouseScroll(50, -1)
        time.sleep(1)
        self.DetectDailyTasks(crop)
        dataClientMgr.dailyTasksHasBeenChecked = True

    @staticmethod
    def DetectDailyTasks(crop):
        screenClientMgr.TakeScreenshot(crop=crop)
        result = ocrClientMgr.mOcr.RecognizeMultiLines(screenClientMgr.mDetect.screenshot)
        for box in result:
            text = box[1][0]
            for keyword, taskName in dataClientMgr.meta["task_mappings"].items():
                if keyword in text:
                    if taskName in dataClientMgr.tempDailyTasksList[dataClientMgr.currentUid] and dataClientMgr.tempDailyTasksList[dataClientMgr.currentUid][taskName] == False:
                        continue
                    else:
                        dataClientMgr.tempDailyTasksList[dataClientMgr.currentUid][taskName] = True
                    break
    
    