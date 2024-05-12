from States.Base.BaseState import BaseState
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.ScreenClientHotaru import screenClientMgr
from Hotaru.Client.DataClientHotaru import dataClientMgr
import time

class BaseClientState(BaseState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseClientState'
    
    @staticmethod
    def CalcDailyTasksScore():
        configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataClientMgr.currentUid] = 0
        tempScore = 0
        i=0
        for key, value in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid].items():
            # Utils._content.update({f'daily_0{i}_score':f'{Utils._task_score_mappings[key]}'})
            i+=1
            if not value:
                tempScore += dataClientMgr.meta['task_score_mappings'][key]
        
        if tempScore >= 500:
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataClientMgr.currentUid] = 500
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataClientMgr.currentUid] = True
            return configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataClientMgr.currentUid]
        elif not configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataClientMgr.currentUid]:
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataClientMgr.currentUid] = tempScore

        return configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataClientMgr.currentUid]
    
    @staticmethod
    def ChangeTeam(team):
        teamName = f"0{str(team)}"
        log.info(logMgr.Info(f"准备切换到队伍{teamName}"))
        screenClientMgr.ChangeTo("configure_team")

        def SelectTeam():
            if screenClientMgr.ClickElement(teamName, "text", maxRetries=3, crop=(311.0 / 1920, 15.0 / 1080, 1376.0 / 1920, 100.0 / 1080)):
                # 等待界面切换
                time.sleep(1)
                result = screenClientMgr.FindElement(("已启用", "启用队伍", "快速编队", "开始挑战"), "text", maxRetries=3, crop=(1507.0 / 1920, 955.0 / 1080, 336.0 / 1920, 58.0 / 1080))
                if result:
                    if screenClientMgr.mDetect.matchedText == "开始挑战":
                        log.info(logMgr.Info(f"正在使用队伍{teamName}进行挑战"))
                        return True
                    elif screenClientMgr.mDetect.matchedText == "已启用":
                        log.info(logMgr.Info(f"已经是队伍{teamName}了"))
                        screenClientMgr.ChangeTo("main")
                        return True
                    elif screenClientMgr.mDetect.matchedText == "启用队伍":
                        screenClientMgr.ClickElementWithPos(result)
                        if screenClientMgr.FindElement("已启用", "text", maxRetries=10, crop=(1507.0 / 1920, 955.0 / 1080, 336.0 / 1920, 58.0 / 1080)):
                            log.info(logMgr.Info(f"切换到队伍{teamName}成功"))
                            return True
                    elif screenClientMgr.mDetect.matchedText == "快速编队":
                        log.error(logMgr.Error("该队伍编号没有设置任何角色,取消切换队伍"))
                        return True
            else:
                return False
                        
        if screenClientMgr.FindElement("./assets/static/images/menu/configure_team_ui.png", "image", 0.9, 3):
            point = screenClientMgr.FindElement("./assets/static/images/menu/configure_team_ui.png", "image", 0.9, 3)
            teamTopLeftX = point[0][0]
            teamTopLeftY = point[0][1]
            screenClientMgr.MouseMove(teamTopLeftX + 800, teamTopLeftY)
            if SelectTeam():
                return True
            else:
                screenClientMgr.MouseScroll(10, -1 if (team - 5) >= 0 else 1)
                if SelectTeam():
                    return True
                else:
                    screenClientMgr.MouseScroll(10, 1 if (team - 5) >= 0 else -1)
                    return SelectTeam()
            
        return False
    
    @staticmethod
    def BorrowCharacter():
        if not (("使用支援角色并获得战斗胜利1次" in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid] and configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid]["使用支援角色并获得战斗胜利1次"]) or configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER_ENABLE][dataClientMgr.currentUid]):
            return True
        if not screenClientMgr.ClickElement("支援", "text", maxRetries=10, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            log.error(logMgr.Error("找不到支援按钮"))
            return False
        # 等待界面加载
        time.sleep(0.5)
        if not screenClientMgr.FindElement("支援列表", "text", maxRetries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080)):
            log.error(logMgr.Error("未进入支援列表"))
            return False

        try:
            for name in configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER]:
                if screenClientMgr.ClickElement("./assets/static/images/character/" + name + ".png", "image", 0.8, maxRetries=1, scaleRange=(0.9, 0.9), crop=(57 / 1920, 143 / 1080, 140 / 1920, 814 / 1080)):
                    if not screenClientMgr.ClickElement("入队", "text", maxRetries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                        log.error(logMgr.Error("找不到入队按钮"))
                        return False
                    # 等待界面加载
                    time.sleep(0.5)
                    result = screenClientMgr.FindElement(("解除支援", "取消"), "text", maxRetries=10, include=True)
                    if result:
                        if screenClientMgr.mDetect.matchedText == "解除支援":
                            configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid]["使用支援角色并获得战斗胜利1次"] = False
                            return True
                        elif screenClientMgr.mDetect.matchedText == "取消":
                            screenClientMgr.ClickElementWithPos(result)
                            screenClientMgr.FindElement("支援列表", "text", maxRetries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080))
                            continue
                    else:
                        return False
        except Exception as e:
            log.warning(logMgr.Warning(f"选择支援角色出错： {e}"))

        screenClientMgr.PressKey("esc")
        if screenClientMgr.FindElement("解除支援", "text", maxRetries=2, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            return True
        else:
            return False
