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

    class Fight:
        @staticmethod
        def WaitFight(instanceName):
            if not screenMgr.FindElement("./assets/images/base/2x_speed_on.png", "image", 0.9, crop=(1618.0 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
                log.info(logMgr.Info("尝试开启二倍速"))
                screenMgr.PressKey("b")
                time.sleep(0.5)
            elif not screenMgr.FindElement("./assets/images/base/not_auto.png", "image", 0.9, crop=(1618.0 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
                log.info(logMgr.Info("尝试开启自动战斗"))
                screenMgr.PressKey("v")
                time.sleep(0.5)
            elif screenMgr.FindElement("./assets/images/fight/fight_again.png", "image", 0.9):
                log.info(logMgr.Info("检测到战斗结束"))
                time.sleep(0.5)
                return
            elif screenMgr.FindElement("./assets/images/fight/fight_fail.png", "image", 0.9):
                log.info(logMgr.Info("检测到战斗失败/重试"))
                time.sleep(0.5)
                nowtime = time.time()
                log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时或战败"))
                raise Exception(f"{nowtime},挑战{instanceName}时战斗超时或战败")

        @staticmethod
        def RunInstances(instanceType, instanceName, aTimesNeedPower, totalCount):
            if instanceName == "无":
                log.warning(logMgr.Warning(f"{instanceType}未开启"))
                return False

            instanceName = instanceName.replace("巽风之形", "风之形")
            instanceName = instanceName.replace("翼风之形", "风之形")

            instanceName = instanceName.replace("偃偶之形", "偶之形")
            instanceName = instanceName.replace("孽兽之形", "兽之形")

            instanceName = instanceName.replace("燔灼之形", "灼之形")
            instanceName = instanceName.replace("潘灼之形", "灼之形")
            instanceName = instanceName.replace("熠灼之形", "灼之形")
            instanceName = instanceName.replace("蛀星的旧靥", "蛀星的旧")

            if configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_ENABLE][dataMgr.currentUid]:
                BaseState.ChangeTeam(configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][dataMgr.currentUid])

            screenMgr.ChangeTo('guide3')
            instanceTypeCrop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
            if not screenMgr.ClickElement(instanceType, "text", crop=instanceTypeCrop):
                if screenMgr.ClickElement("侵蚀隧洞", "text", maxRetries=10, crop=instanceTypeCrop):
                    screenMgr.MouseScroll(12, -1)
                    time.sleep(0.5)
                    screenMgr.ClickElement(instanceType, "text", crop=instanceTypeCrop)
            # 截图过快会导致结果不可信
            time.sleep(1)

            # 传送
            instanceNameCrop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
            screenMgr.ClickElement("./assets/images/screen/guide/power.png", "image", maxRetries=10)
            Flag = False
            instance_map_type = ''
            import json
            rb = open("./assets/config/ruby_detail.json", 'r', encoding='utf-8')
            ruby = json.load(rb)
            rb.close()

            if instanceType in ['拟造花萼（赤）']:
                source = f"./assets/images/screen/guide/aka/{ruby['拟造花萼（赤）'][instanceName]}.png"
                for i in range(7):
                    if screenMgr.ClickElement("传送", "min_distance_text", crop=instanceNameCrop, include=True, source=source,  source_type="image"):
                        Flag = True
                        break

                    elif screenMgr.ClickElement("进入", "min_distance_text", crop=instanceNameCrop, include=True, source=source,  source_type="image"):
                        log.info("该副本限时开放中,但你并没有解锁该副本")
                        Flag = True
                        break

                    if screenMgr.ClickElement("追踪", "min_distance_text", crop=instanceNameCrop, include=True, source=source,  source_type="image"):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                        raise Exception(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本")
                        
                    screenMgr.MouseScroll(18, -1)
                    # 等待界面完全停止
                    time.sleep(1)
            elif instanceType in ['拟造花萼（金）']:

                instance_map, instance_map_type = instanceName.split('-')
                instance_map_name = ruby['星球'][instance_map]

                for i in range(2):
                    if screenMgr.ClickElement(f"./assets/images/screen/guide/{instance_map_name}_on.png", "image", 0.9, maxRetries=10) or screenMgr.ClickElement(f"./assets/images/screen/guide/{instance_map_name}_off.png", "image", 0.9, maxRetries=10):

                        if screenMgr.ClickElement("传送", "min_distance_text", crop=instanceNameCrop, include=True, source=instance_map_type):
                            Flag = True
                            break

                        elif screenMgr.ClickElement("进入", "min_distance_text", crop=instanceNameCrop, include=True, source=instance_map_type, source_type="text"):
                            log.info("该副本限时开放中,但你并没有解锁该副本")
                            Flag = True
                            break

                        if screenMgr.ClickElement("追踪", "min_distance_text", crop=instanceNameCrop, include=True, source=instance_map_type, source_type="text"):
                            nowtime = time.time()
                            log.error(logMgr.Error(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                            raise Exception(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本")
                        
                    # 等待界面完全停止
                    time.sleep(1)     
            else:
                for i in range(7):
                    if screenMgr.ClickElement("传送", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceName, source_type="text"):
                        Flag = True
                        break
                    elif screenMgr.ClickElement("进入", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceName, source_type="text"):
                        log.info("该副本限时开放中,但你并没有解锁该副本")
                        Flag = True
                        break

                    if screenMgr.ClickElement("追踪", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceName, source_type="text"):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},{instanceName}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                        raise Exception(f"{nowtime},{instanceName}:你似乎没有解锁这个副本?总之无法传送到该副本")
                    screenMgr.MouseScroll(18, -1)
                    # 等待界面完全停止
                    time.sleep(1)
                
            if not Flag:
                log.error(logMgr.Error("⚠️刷副本未完成 - 没有找到指定副本名称⚠️"))

                return False
            # 验证传送是否成功
            if not screenMgr.FindElement(instanceName.replace("2", ""), "text", maxRetries=20, include=True, crop=(1172.0 / 1920, 5.0 / 1080, 742.0 / 1920, 636.0 / 1080)):
                if not screenMgr.FindElement(instance_map_type, "text", maxRetries=20, include=True, crop=(1172.0 / 1920, 5.0 / 1080, 742.0 / 1920, 636.0 / 1080)):
                    log.error(logMgr.Error("⚠️刷副本未完成 - 传送可能失败⚠️"))
                    return False

            fullCount = totalCount // 6
            incomplete_count = totalCount - fullCount * 6
            log.info(logMgr.Info(f"按单次体力需求计算次数:{totalCount},按6次为完整一次计算:{fullCount},按扣除完整次数剩下次数计算:{incomplete_count}"))
            if "拟造花萼" in instanceType:
                
                if not 0 <= fullCount or not 0 <= incomplete_count <= 6:
                    log.error(logMgr.Error("⚠️刷副本未完成 - 拟造花萼次数错误⚠️"))
                    # Base.send_notification_with_screenshot(_("⚠️刷副本未完成 - 拟造花萼次数错误⚠️"))
                    return False
                result = screenMgr.FindElement("./assets/images/screen/guide/plus.png", "image", 0.9, maxRetries=10,
                                        crop=(1174.0 / 1920, 775.0 / 1080, 738.0 / 1920, 174.0 / 1080))
                if fullCount == 0:
                    for i in range(incomplete_count - 1):
                        screenMgr.ClickElementWithPos(result)
                        time.sleep(0.5)
                else:
                    for i in range(5):
                        screenMgr.ClickElementWithPos(result)
                        time.sleep(0.5)

            if screenMgr.ClickElement("挑战", "text", maxRetries=10, need_ocr=True):
                if instanceType == "历战余响":
                    time.sleep(1)
                    screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9)

                if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid] == False:
                    BaseState.BorrowCharacter()
                if screenMgr.ClickElement("开始挑战", "text", maxRetries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                    time.sleep(1)

                    if screenMgr.FindElement("./assets/images/fight/no_power.png", "image", 0.9):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时开拓力不足,但却触发了挑战,请检查"))
                        raise Exception(f"{nowtime},挑战{instanceName}时开拓力不足,但却触发了挑战,请检查")
                    
                    if screenMgr.FindElement("./assets/images/fight/char_dead.png", "image", 0.9):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时有角色处于无法战斗的状态,请检查"))
                        raise Exception(f"{nowtime},挑战{instanceName}时有角色处于无法战斗的状态,请检查")
                    
                    if instanceType in ["凝滞虚影", "侵蚀隧洞", "历战余响"]:
                        time.sleep(2)
                        if instanceType in ["凝滞虚影"]:
                            for i in range(3):
                                screenMgr.PressMouse()
                                time.sleep(3)

                        for i in range(totalCount - 1):

                            Retry.ReThread(lambda: BaseState.Fight.WaitFight(instanceName), 300, 1)

                            log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(1)"))
                            if instanceType == "侵蚀隧洞":
                                BaseState.Relics.InstanceGetRelic()
                            time.sleep(1)
                            screenMgr.ClickElement("./assets/images/fight/fight_again.png", "image", 0.9, maxRetries=10)
                            if instanceType == "历战余响":
                                time.sleep(1)
                                screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9) 
                            time.sleep(1) 
                    else:
                        if fullCount > 0:
                            for i in range(fullCount - 1):

                                Retry.ReThread(lambda: BaseState.Fight.WaitFight(instanceName), 300, 1)

                                log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(2)"))
                                if not (fullCount == 1 and incomplete_count == 0):
                                    screenMgr.ClickElement("./assets/images/fight/fight_again.png", "image", 0.9, maxRetries=10)
                                    # if instance_type == "历战余响":
                                    #     time.sleep(1)
                                    #     screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9)  
                    
                    Retry.ReThread(lambda: BaseState.Fight.WaitFight(instanceName), 300, 1)

                    if instanceType == "侵蚀隧洞":
                        BaseState.Relics.InstanceGetRelic()
                    if fullCount > 0:
                        log.info(logMgr.Info(f"{fullCount*6}次{instanceType}副本完成(3)"))
                    elif instanceType == "凝滞虚影" or "侵蚀隧洞" :
                        log.info(logMgr.Info(f"{totalCount}次{instanceType}副本完成(4)"))
                    else:
                        log.info(logMgr.Info(f"{incomplete_count}次{instanceType}副本完成(5)"))
                    # 速度太快，点击按钮无效
                    time.sleep(1)
                    screenMgr.ClickElement("./assets/images/fight/fight_exit.png", "image", 0.9, maxRetries=10)
                    time.sleep(2)
                    if fullCount > 0 and incomplete_count > 0:
                        BaseState.RunInstances(instanceType, instanceName, aTimesNeedPower, incomplete_count)
                    else:
                        log.info(logMgr.Info("副本任务完成"))
                        return True
    
    class Relics:
        @staticmethod
        def InstanceGetRelic():
            relic_name_crop=(783.0 / 1920, 318.0 / 1080, 436.0 / 1920, 53.0 / 1080) # 遗器名称
            relic_prop_crop=(831.0 / 1920, 398.0 / 1080, 651.0 / 1920, 181.0 / 1080) # 遗器属性
            log.info(logMgr.Info("开始检测遗器"))

            point = screenMgr.FindElement("./assets/images/fight/fight_reward.png", "image", 0.9, maxRetries=2)
            
            success_reward_top_left_x = point[0][0]
            success_reward_top_left_y = point[0][1]

            for i in range(2):
                for j in range(7):

                    screenMgr.ClickElementWithPos(((success_reward_top_left_x -380 + j *120, success_reward_top_left_y + 40 + i * 120), (success_reward_top_left_x -380 + 120 + j *120, success_reward_top_left_y + 40 + 120 + i * 120)))
                        
                    if not screenMgr.FindElement("./assets/images/fight/5star.png", "image", 0.9, maxRetries=2):
                        if screenMgr.ClickElement("./assets/images/fight/relic_info_close.png", "image", 0.9, maxRetries=3):
                            time.sleep(0.5)
                        else:
                            break
                    else:
                        time.sleep(0.5)
                        relic_name = screenMgr.GetSingleLineText(relic_name_crop, blacklist=[], maxRetries=5)

                        relic_part = screenMgr.GetSingleLineText(crop=(515.0 / 1920, 726.0 / 1080, 91.0 / 1920, 35.0 / 1080),blacklist=['+','0'],maxRetries=3)
                        log.info(logMgr.Info(f"{relic_name}:{relic_part}"))

                        screenMgr.TakeScreenshot(crop=relic_prop_crop)
                        time.sleep(0.5)
                        
                        isProp = False
                        tempMainPropName = ''
                        propCount = -1
                        usefulPropCount = 0
                        relicList = list()
                        isMainProp = True

                        result = ocrMgr.mOcr.RecognizeMultiLines(screenMgr.mDetect.screenshot)
                        time.sleep(0.5)

                        tempListValue = ''

                        for box in result:
                            text = box[1][0]
                            if text in ['暴击率','暴击伤害','生命值','攻击力','防御力','能量恢复效率','效果命中','效果抵抗','速度','击破特攻','治疗量加成','量子属性伤害加成','风属性伤害加成','火属性伤害加成','雷属性伤害加成','冰属性伤害加成','虚数属性伤害加成']:
                                if isMainProp:
                                    tempMainPropName = text
                                tempListValue = f'{text}:'
                                isProp = True
                                if text in ['暴击率','暴击伤害']:
                                    usefulPropCount += 1
                                continue
                            elif isProp:
                                if isMainProp:
                                    isMainProp = False
                                # tempPropValue = text
                                tempListValue += f'{text}'
                                isProp = False
                                propCount += 1
                            else:
                                continue
                            # logger.info(f"{tempListValue}")
                            relicList.append(tempListValue)
                        
                        # logger.info(f"{propCount}")
                        # logger.info(f"{usefulPropCount}")
                        allPropText = '词条:'
                        for key in relicList:
                            allPropText += f'{key},'
                        log.info(logMgr.Info(allPropText))
                        log.info(logMgr.Info(f"总词条数:{propCount},有效词条:{usefulPropCount}"))

                        BaseState.Relics.IsGoodRelic(relic_name, relic_part, relicList, propCount, usefulPropCount, tempMainPropName)
                        
                        time.sleep(0.5)
                        if screenMgr.ClickElement("./assets/images/fight/relic_info_close.png", "image", 0.9, maxRetries=3):
                            time.sleep(0.5)

        @staticmethod
        def IsGoodRelic():
            pass
