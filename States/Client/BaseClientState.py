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
    def DownloadChar(isUniverse=False):
        if isUniverse:
            scrollText = "universe"
            scrollTopThreshold = 0.9999
            scrollBottomThreshold = 0.99
            if screenClientMgr.ClickElement("./assets/static/images/screen/universe/download_char.png", "image", 0.9,maxRetries=5):
                time.sleep(1)
                BaseClientState.ClearTeam(1, isUniverse)
            else:
                BaseClientState.ThrowException("差分宇宙未找到下载角色按钮")
        else:
            scrollText = "ornament"
            scrollTopThreshold = 0.9999
            scrollBottomThreshold = 0.9997
            BaseClientState.ClearTeam(1, isUniverse)

        def SelectChar(charList:list):

            # -1为往下,1为往上
            def RepeatScroll(_character):
                time.sleep(1)
                if not screenClientMgr.ClickElement(f"./assets/static/images/character/{_character}.png", "image", 0.85, maxRetries=3, takeScreenshot=True):
                    point = screenClientMgr.FindElement("./assets/static/images/synthesis/filter.png", "image", 0.9, maxRetries=3)

                    scrollViewTopLeftX = point[0][0]
                    scrollViewTopLeftY = point[0][1]
                    screenClientMgr.MouseMove(scrollViewTopLeftX, scrollViewTopLeftY - 200)

                    time.sleep(0.5)
                    screenClientMgr.MouseScroll(25, -1)

                    time.sleep(1)
                    if not screenClientMgr.ClickElement(f"./assets/static/images/character/{_character}.png", "image", 0.85, maxRetries=3, takeScreenshot=True):
                        if screenClientMgr.FindElement(f"./assets/static/images/screen/{scrollText}_scrollBottom.png", "image", scrollBottomThreshold, crop=(507.0 / 1920, 849.0 / 1080, 108.0 / 1920, 97.0 / 1080)):
                            log.warning(logMgr.Warning("角色列表已到底,仍未选中该角色"))
                            return False
                        else:
                            screenClientMgr.MouseScroll(25, -1)
                            return RepeatScroll(_character)
                    else:
                        log.info(logMgr.Info("该角色已选中"))
                        for i in range(10):
                            if not screenClientMgr.FindElement(f"./assets/static/images/screen/{scrollText}_scrollTop.png", "image", scrollTopThreshold, crop=(505.0 / 1920, 110.0 / 1080, 84.0 / 1920, 96.0 / 1080)):
                                screenClientMgr.MouseScroll(25, 1)
                            else:
                                break

                        return True
                else:
                    log.info(logMgr.Info("该角色已选中"))
                    for j in range(10):
                        if not screenClientMgr.FindElement(f"./assets/static/images/screen/{scrollText}_scrollTop.png", "image", scrollTopThreshold, crop=(505.0 / 1920, 110.0 / 1080, 84.0 / 1920, 96.0 / 1080)):
                            screenClientMgr.MouseScroll(25, 1)
                        else:
                            break

                    return True

            charCount = 0
            for character in charList:
                if charCount == 4:
                    break

                log.info(logMgr.Info(f"正在尝试选中:{(dataClientMgr.meta['角色'][character]).split(':')[1]}"))

                if RepeatScroll(character):
                    charCount+=1
                    
            if charCount == 4:
                return False
            else:
                log.info(logMgr.Info(f"{charCount}"))
                BaseClientState.ThrowException("未能选中4位配置中的角色,请检查")

        if isUniverse:
            SelectChar(configMgr.mConfig[configMgr.mKey.UNIVERSE_TEAM][dataClientMgr.currentUid])
        else:
            SelectChar(configMgr.mConfig[configMgr.mKey.ORNAMENT_EXTRACTION_TEAM][dataClientMgr.currentUid])

    @staticmethod
    def ClearTeam(j, isUniverse=False):
        if j == 3:
            BaseClientState.ThrowException("清理队伍失败")
        
        point = screenClientMgr.FindElement("下载角色", "text", 0.9, maxRetries=2)
        downloadCharTopLeftX = point[0][0]
        downloadCharTopLeftY = point[0][1]

        screenClientMgr.ClickElementWithPos(((downloadCharTopLeftX + 60, downloadCharTopLeftY), (downloadCharTopLeftX + 60, downloadCharTopLeftY + 80)))
        time.sleep(1)
        
        for i in range(4):  
            screenClientMgr.ClickElementWithPos(((downloadCharTopLeftX + 60 + i*105, downloadCharTopLeftY + 80), (downloadCharTopLeftX + 60 + i*105, downloadCharTopLeftY + 80)))
            time.sleep(1)
        
        if isUniverse:
            text = 'universe'
        else:
            text = 'ornament'

        if screenClientMgr.FindElement(f"./assets/static/images/{text}/all_clear_team.png", "image", 0.95, takeScreenshot=True):
            log.info(logMgr.Info("队伍已清空"))
            return
        else:
            BaseClientState.ClearTeam(j+1, isUniverse)
    
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
                        if screenClientMgr.FindElement("已启用", "text", maxRetries=3, crop=(1507.0 / 1920, 955.0 / 1080, 336.0 / 1920, 58.0 / 1080)):
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
    def ThrowException(content):
        nowtime = time.time()
        log.error(logMgr.Error(f"{nowtime},{content}"))
        screenClientMgr.TakeSpecialScreenshot(isException = True)
        raise Exception(f"{nowtime},{content}")
    
    @staticmethod
    def BorrowCharacter():
        if not (("使用支援角色并获得战斗胜利1次" in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid] and configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid]["使用支援角色并获得战斗胜利1次"]) or configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER_ENABLE][dataClientMgr.currentUid]):
            return True
        if not screenClientMgr.ClickElement("支援", "text", maxRetries=3, crop=(990.0 / 1920, 575.0 / 1080, 900.0 / 1920, 285.0 / 1080)):
            log.error(logMgr.Error("找不到支援按钮"))
            return False
        # 等待界面加载
        time.sleep(0.5)
        if not screenClientMgr.FindElement("支援列表", "text", maxRetries=3, crop=(243.0 / 1920, 47.0 / 1080, 109.0 / 1920, 100.0 / 1080)):
            log.error(logMgr.Error("未进入支援列表"))
            return False

        try:
            for name in configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER]:
                if screenClientMgr.ClickElement("./assets/static/images/character/" + name + ".png", "image", 0.5, maxRetries=1, scaleRange=(0.9, 0.9), crop=(37 / 1920, 143 / 1080, 140 / 1920, 814 / 1080)):
                    if not screenClientMgr.ClickElement("入队", "text", maxRetries=3, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                        log.error(logMgr.Error("找不到入队按钮"))
                        return False
                    # 等待界面加载
                    time.sleep(0.5)
                    result = screenClientMgr.FindElement(("解除支援", "取消"), "text", maxRetries=3, include=True)
                    if result:
                        if screenClientMgr.mDetect.matchedText == "解除支援":
                            configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid]["使用支援角色并获得战斗胜利1次"] = False
                            return True
                        elif screenClientMgr.mDetect.matchedText == "取消":
                            screenClientMgr.ClickElementWithPos(result)
                            screenClientMgr.FindElement("支援列表", "text", maxRetries=3, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080))
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
