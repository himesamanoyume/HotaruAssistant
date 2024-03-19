from States import *

class BaseState(object):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseState'

    def OnBegin(self):
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    @staticmethod
    def CalcDailyTasksScore():
        configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataMgr.currentUid] = 0
        tempScore = 0
        i=0
        for key, value in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid].items():
            # Utils._content.update({f'daily_0{i}_score':f'{Utils._task_score_mappings[key]}'})
            i+=1
            if not value:
                tempScore += dataMgr.meta['task_score_mappings'][key]
        
        if tempScore >= 500:
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataMgr.currentUid] = 500
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid] = True
            return configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataMgr.currentUid]
        elif not configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid]:
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataMgr.currentUid] = tempScore

        return configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataMgr.currentUid]
    
    @staticmethod
    def ChangeTeam(team):
        teamName = f"0{str(team)}"
        log.info(logMgr.Info(f"准备切换到队伍{teamName}"))
        screenMgr.ChangeTo("configure_team")
        if screenMgr.ClickElement(teamName, "text", maxRetries=10, crop=(311.0 / 1920, 15.0 / 1080, 1376.0 / 1920, 100.0 / 1080)):
            # 等待界面切换
            time.sleep(1)
            result = screenMgr.FindElement(("已启用", "启用队伍"), "text", maxRetries=10, crop=(1507.0 / 1920, 955.0 / 1080, 336.0 / 1920, 58.0 / 1080))
            if result:
                if screenMgr.mDetect.matchedText == "已启用":
                    log.info(logMgr.Info(f"已经是队伍{teamName}了"))
                    screenMgr.ChangeTo("main")
                    return True
                elif screenMgr.mDetect.matchedText == "启用队伍":
                    screenMgr.ClickElementWithPos(result)
                    if screenMgr.FindElement("已启用", "text", maxRetries=10, crop=(1507.0 / 1920, 955.0 / 1080, 336.0 / 1920, 58.0 / 1080)):
                        log.info(logMgr.Info(f"切换到队伍{teamName}成功"))
                        return True
        return False
    
    @staticmethod
    def BorrowCharacter():
        if not (("使用支援角色并获得战斗胜利1次" in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid] and configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid]["使用支援角色并获得战斗胜利1次"]) or configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER_ENABLE]):
            return True
        if not screenMgr.ClickElement("支援", "text", maxRetries=10, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            log.error(logMgr.Error("找不到支援按钮"))
            return False
        # 等待界面加载
        time.sleep(0.5)
        if not screenMgr.FindElement("支援列表", "text", maxRetries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080)):
            log.error(logMgr.Error("未进入支援列表"))
            return False

        try:
            # 尝试优先使用指定用户名的支援角色
            if configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER_FROM]:
                screenMgr.ClickElement("UID", "text", maxRetries=10, crop=(18.0 / 1920, 15.0 / 1080, 572.0 / 1920, 414.0 / 1080), include=True)
                time.sleep(0.5)
                for i in range(3):
                    if screenMgr.ClickElement(configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER_FROM], "text", crop=(196 / 1920, 167 / 1080, 427 / 1920, 754 / 1080), include=True):
                        # 找到角色的对应处理
                        if not screenMgr.ClickElement("入队", "text", maxRetries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                            log.error(logMgr.Error("找不到入队按钮"))
                            return False
                        # 等待界面加载
                        time.sleep(0.5)
                        result = screenMgr.FindElement(("解除支援", "取消"), "text", maxRetries=10, include=True)
                        if result:
                            if screenMgr.mDetect.matchedText == "解除支援":
                                if "使用支援角色并获得战斗胜利1次" in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid]:
                                    configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid]["使用支援角色并获得战斗胜利1次"] = False
                                return True
                            elif screenMgr.mDetect.matchedText == "取消":
                                screenMgr.ClickElementWithPos(result)
                                screenMgr.FindElement("支援列表", "text", maxRetries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080))
                                continue
                        else:
                            return False
                    screenMgr.MouseScroll(27, -1)
                    # 等待界面完全停止
                    time.sleep(1)

                log.info(logMgr.Info("找不到指定用户名的支援角色，尝试按照优先级选择"))
                # 重新打开支援页面，防止上一次的滚动位置影响
                screenMgr.PressKey("esc")
                time.sleep(0.5)
                if not screenMgr.ClickElement("支援", "text", maxRetries=10, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
                    log.error(logMgr.Error("找不到支援按钮"))
                    return False
                # 等待界面加载
                time.sleep(0.5)
                if not screenMgr.FindElement("支援列表", "text", maxRetries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080)):
                    log.error(logMgr.Error("未进入支援列表"))
                    return False

            for name in configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER]:
                if screenMgr.ClickElement("./assets/images/character/" + name + ".png", "image", 0.8, maxRetries=1, scale_range=(0.9, 0.9), crop=(57 / 1920, 143 / 1080, 140 / 1920, 814 / 1080)):
                    if not screenMgr.ClickElement("入队", "text", maxRetries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                        log.error(logMgr.Error("找不到入队按钮"))
                        return False
                    # 等待界面加载
                    time.sleep(0.5)
                    result = screenMgr.FindElement(("解除支援", "取消"), "text", maxRetries=10, include=True)
                    if result:
                        if screenMgr.mDetect.matchedText == "解除支援":
                            configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid]["使用支援角色并获得战斗胜利1次"] = False
                            return True
                        elif screenMgr.mDetect.matchedText == "取消":
                            screenMgr.ClickElementWithPos(result)
                            screenMgr.FindElement("支援列表", "text", maxRetries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080))
                            continue
                    else:
                        return False
        except Exception as e:
            log.warning(logMgr.Warning(f"选择支援角色出错： {e}"))

        screenMgr.PressKey("esc")
        if screenMgr.FindElement("解除支援", "text", maxRetries=2, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            return True
        else:
            return False
