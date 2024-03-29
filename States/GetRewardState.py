from States import *

class GetRewardState(object):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'DailyGetRewardState'

    def OnBegin(self):
        log.hr(logMgr.Hr("开始领奖励"), 0)
        screenMgr.ChangeTo('menu')

        rewardList = []

        rewardMapping = {
            "mail": lambda: screenMgr.FindElement("./assets/images/menu/mail_reward.png", "image", 0.9, takeScreenshot=False, crop=(0.95, 0.1, 0.05, 0.6)),
            "assist": lambda: screenMgr.FindElement("./assets/images/menu/assist_reward.png", "image", 0.9, takeScreenshot=False),
            "dispatch": lambda: screenMgr.FindElement("./assets/images/menu/dispatch_reward.png", "image", 0.95, takeScreenshot=False),
            # "quest": lambda: screenMgr.FindElement("./assets/images/menu/quest_reward.png", "image", 0.95, take_screenshot=False),
            # "srpass": lambda: screenMgr.FindElement("./assets/images/menu/pass_reward.png", "image", 0.95, take_screenshot=False),
        }

        for rewardName, rewardFunction in rewardMapping.items():
            if rewardFunction():
                rewardList.append(rewardName)

        flag = False
        if len(rewardList) != 0:
            flag = True
            if "mail" in rewardList:
                log.hr(logMgr.Hr("检测到邮件奖励"), 2)
                self.GetMailReward()
                log.info(logMgr.Info("邮件奖励完成"))
            if "assist" in rewardList:
                log.hr(logMgr.Hr("检测到支援奖励"), 2)
                self.GetAssistReward()
                log.info(logMgr.Info("支援奖励完成"))
            if "dispatch" in rewardList:
                log.hr(logMgr.Hr("检测到委托奖励"), 2)
                self.GetDispatchReward(dataMgr.currentUid)
                log.info(logMgr.Info("委托奖励完成"))

        # 每日实训和无名勋礼需要实时检测
        screenMgr.ChangeTo('menu')
        if screenMgr.FindElement("./assets/images/menu/quest_reward.png", "image", 0.95):
            flag = True
            log.hr(logMgr.Hr("检测到每日实训奖励"), 2)
            self.GetQuestReward()
            log.info(logMgr.Info("领取每日实训奖励完成"))
        screenMgr.ChangeTo('menu')
        if screenMgr.FindElement("./assets/images/menu/pass_reward.png", "image", 0.95):
            flag = True
            log.hr(logMgr.Hr("检测到无名勋礼奖励"), 2)
            GetRewardState.GetPassReward()
            log.info(logMgr.Info("领取无名勋礼奖励完成"))

        if not flag:
            log.info(logMgr.Info("未检测到任何奖励"))

        log.hr(logMgr.Hr("领取奖励结束"), 2)

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    @staticmethod
    def GetQuestReward():
        screenMgr.ChangeTo('guide2')
        time.sleep(1)
        # 领取活跃度
        while screenMgr.ClickElementQuest("./assets/images/quest/receive.png", "image", 0.9, crop=(284.0 / 1920, 785.0 / 1080, 274.0 / 1920, 93.0 / 1080)):
            time.sleep(1)
        # 领取奖励
        if screenMgr.ClickElement("./assets/images/quest/gift.png", "image", 0.9, maxRetries=10, crop=(415.0 / 1920, 270.0 / 1080, 1252.0 / 1920, 114.0 / 1080)):
            time.sleep(1)
            screenMgr.ClickElement("./assets/images/base/click_close.png", "image", 0.9, maxRetries=10)
        time.sleep(1)
        screenMgr.FindElement("./assets/images/screen/guide/guide2.png", "image", 0.9, maxRetries=10)
        # 判断完成
        BaseState.CalcDailyTasksScore()
        if screenMgr.FindElement("./assets/images/quest/500.png", "image", 0.95, crop=(415.0 / 1920, 270.0 / 1080, 1252.0 / 1920, 114.0 / 1080)):
            # config.set_value("daily_tasks", {})
            log.info(logMgr.Info("🎉每日实训已完成🎉"))
            # Base.send_notification_with_screenshot(_("🎉每日实训已完成🎉"))
        else:
            log.warning(logMgr.Warning("⚠️每日实训未完成⚠️"))
            # Base.send_notification_with_screenshot(_("⚠️每日实训未完成⚠️"))
    
    @staticmethod
    def GetMailReward():
        if not configMgr.mConfig[configMgr.mKey.MAIL_ENABLE]:
            log.info(logMgr.Info("邮件奖励未开启"))
            return False

        screenMgr.ChangeTo('mail')
        if screenMgr.ClickElement("./assets/images/mail/receive_all.png", "image", 0.9):
            screenMgr.ClickElement("./assets/images/base/click_close.png", "image", 0.9, maxRetries=10)

    @staticmethod
    def GetDispatchReward(uid):
        if not configMgr.mConfig[configMgr.mKey.DISPATCH_ENABLE]:
            log.info(logMgr.Info("委托未开启"))
            return False

        screenMgr.ChangeTo('dispatch')
        # 适配低性能电脑，中间的界面不一定加载出了
        screenMgr.FindElement("专属材料", "text", maxRetries=10, crop=(298.0 / 1920, 153.0 / 1080, 1094.0 / 1920, 122.0 / 1080))
        GetRewardState.PerformDispatches()
        if "派遣1次委托" in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][uid] and configMgr.mConfig[configMgr.mKey.DAILY_TASKS][uid]["派遣1次委托"]:
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS][uid]["派遣1次委托"] = False

    @staticmethod
    def PerformDispatches():
        log.info(logMgr.Info(f"正在进行委托"))

        if not GetRewardState.PerformDispatchAndCheck(crop=(298.0 / 1920, 153.0 / 1080, 1094.0 / 1920, 122.0 / 1080)):
            return

        # if not GetRewardState.PerformDispatchAndCheck(crop=(660 / 1920, 280 / 1080, 170 / 1920, 600 / 1080)):
        #     return

        screenMgr.ClickElement("./assets/images/dispatch/all_receive.png", "image", 0.9, maxRetries=10)
        screenMgr.ClickElement("./assets/images/dispatch/again.png", "image", 0.9, maxRetries=10)
        time.sleep(4)
            

    @staticmethod
    def PerformDispatchAndCheck(crop):
        if not GetRewardState.ClickCompleteDispatch(crop):
            log.warning(logMgr.Warning("未检测到已完成的委托"))
            return False
        time.sleep(0.5)
        return True

    @staticmethod
    def ClickCompleteDispatch(crop):
        # width, height = screenMgr.get_image_info("./assets/images/dispatch/reward.png")
        # offset = (-2 * width, 2 * height)
        offset = (-34, 34)  # 以后改相对坐标偏移
        return screenMgr.ClickElement("./assets/images/dispatch/reward.png", "image", 0.9, maxRetries=8, offset=offset, crop=crop)

    @staticmethod
    def GetAssistReward():
        if not configMgr.mConfig[configMgr.mKey.ASSIST_ENABLE]:
            log.info(logMgr.Info("支援奖励未开启"))
            return False

        screenMgr.ChangeTo('visa')
        if screenMgr.ClickElement("./assets/images/assist/gift.png", "image", 0.9):
            screenMgr.ClickElement("./assets/images/base/click_close.png", "image", 0.9, maxRetries=10)
    
    @staticmethod
    def GetPassReward():
        # 先判断是否能领取经验
        screenMgr.ChangeTo('pass2')
        time.sleep(1)
        if screenMgr.ClickElement("./assets/images/pass/one_key_receive.png", "image", 0.9):
            # 等待可能出现的升级动画
            time.sleep(2)
        screenMgr.ChangeTo('pass1')
        time.sleep(1)
        # 判断是否解锁了"无名客的荣勋"
        if screenMgr.FindElement("./assets/images/pass/lock.png", "image", 0.9):
            time.sleep(1)
            # 若没解锁则领取奖励
            if screenMgr.ClickElement("./assets/images/pass/one_key_receive.png", "image", 0.9):
                time.sleep(1)
                screenMgr.ClickElement("./assets/images/base/click_close.png", "image", 0.9, maxRetries=10)
                time.sleep(1)
        
        time.sleep(1)
        # 判断是否满级
        if screenMgr.FindElement("./assets/images/pass/50.png", "image", 0.9):
            log.info(logMgr.Info("🎉当前版本无名勋礼已满级🎉"))
    