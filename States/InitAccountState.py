from States import *

class InitAccountState(BaseState):

    mStateName = 'InitAccountState'

    def OnBegin(self):
        uidCrop = (70.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080)
        try:
            dataMgr.currentUid = screenMgr.GetSingleLineText(crop=uidCrop, blacklist=[], maxRetries=9)
            if dataMgr.currentUid == None:
                nowtime = time.time()
                log.error(logMgr.Error(f"未能读取到UID"))
                raise Exception(f"未能读取到UID")
            dataMgr.loopStartTimestamp = time.time()
            log.info(logMgr.Info(f"识别到UID为:{dataMgr.currentUid}"))
            configMgr.mConfig.SetValue(configMgr.mKey.LAST_RUNNING_UID, dataMgr.currentUid)
        except Exception as e:
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},识别UID失败: {e}"))
            raise Exception(f"{nowtime},识别UID失败: {e}")

    def OnRunning(self):
        if Date.IsNext4AM(configMgr.mConfig[configMgr.mKey.LAST_RUN_TIMESTAMP][dataMgr.currentUid]):
            log.info(logMgr.Info("已是新的一天,开始每日"))
            if len(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid]) == 1:
                pass
            else:
                if configMgr.mConfig[configMgr.mKey.LAST_RUN_TIMESTAMP][dataMgr.currentUid] == 0:
                    pass
                else:
                    configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid].remove(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0])

            screenMgr.ChangeTo('activity')
            activityList = []
            screenMgr.TakeScreenshot(crop=(46.0 / 1920, 107.0 / 1080, 222.0 / 1920, 848.0 / 1080))

            result = ocrMgr.mOcr.RecognizeMultiLines(screenMgr.mDetect.screenshot)
            if not result:
                log.info(logMgr.Info("未检测到任何活动"))
                # logger.hr(_("完成"), 2)
                return

            for box in result:
                text = box[1][0]
                if len(text) >= 4:
                    activityList.append(text)
                    # logger.info(text)

            if "巡星之礼" in activityList:
                self.GetReward()
            if "巡光之礼" in activityList:
                self.GetReward()

            screenMgr.ChangeTo("guide2")
            self.StartDetectDailyTasks()
            configMgr.mConfig.SetValue(configMgr.mKey.DAILY_TASKS, dataMgr.tempDailyTasksList)
            configMgr.SaveTimestampByUid(configMgr.mKey.LAST_RUN_TIMESTAMP, dataMgr.currentUid)
        else:
            log.info(logMgr.Info("日常任务\033[91m未刷新\033[0m"))

        self.CalcDailyTasksScore()


    def OnExit(self):
        return False
    
    @staticmethod
    def GetReward():
        screenMgr.ChangeTo('activity')
        if screenMgr.ClickElement("巡星之礼", "text", None, crop=(46.0 / 1920, 107.0 / 1080, 222.0 / 1920, 848.0 / 1080)):
            time.sleep(1)
            receive_path = "./assets/images/activity/giftof/receive.png"
            receive_fin_path = "./assets/images/activity/giftof/receive_fin.png"
            if screenMgr.FindElement(receive_path, "image", 0.9) or screenMgr.FindElement(receive_fin_path, "image", 0.9):
                log.hr(logMgr.Hr("检测到巡星之礼奖励"), 2)
                while screenMgr.ClickElement(receive_path, "image", 0.9) or screenMgr.ClickElement(receive_fin_path, "image", 0.9):
                    screenMgr.ClickElement("./assets/images/base/click_close.png", "image", 0.9, maxRetries=10)
                    time.sleep(1)
                log.info(logMgr.Info("领取巡星之礼奖励完成"))

    def StartDetectDailyTasks(self):
        crop = (243.0 / 1920, 377.0 / 1080, 1428.0 / 1920, 528.0 / 1080)
        if configMgr.mConfig[configMgr.mKey.DAILY_TASKS] == {}:
            dataMgr.tempDailyTasksList = {}
        else:
            dataMgr.tempDailyTasksList = configMgr.mConfig[configMgr.mKey.DAILY_TASKS]

        self.DetectDailyTasks(crop)
        screenMgr.ClickElement("./assets/images/quest/activity.png", "image", 0.95, crop=crop)
        screenMgr.MouseScroll(50, -1)
        time.sleep(0)
        self.DetectDailyTasks(crop)
        dataMgr.dailyTasksHasBeenChecked = True

    @staticmethod
    def DetectDailyTasks(crop):
        screenMgr.TakeScreenshot(crop=crop)
        result = ocrMgr.mOcr.RecognizeMultiLines(screenMgr.mDetect.screenshot)
        for box in result:
            text = box[1][0]
            for keyword, task_name in dataMgr.meta["task_mappings"].items():
                if keyword in text:
                    if task_name in dataMgr.tempDailyTasksList[dataMgr.currentUid] and dataMgr.tempDailyTasksList[dataMgr.currentUid][task_name] == False:
                        continue
                    else:
                        dataMgr.tempDailyTasksList[dataMgr.currentUid][task_name] = True
                    break
    
    