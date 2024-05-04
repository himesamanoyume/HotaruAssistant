from States.Client import *

class BaseRelicsState(BaseClientState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseRelicsState'

    @staticmethod
    def InstanceGetRelics():
        relicsNameCrop=(783.0 / 1920, 318.0 / 1080, 436.0 / 1920, 53.0 / 1080) # 遗器名称
        relicsPropCrop=(831.0 / 1920, 398.0 / 1080, 651.0 / 1920, 181.0 / 1080) # 遗器属性
        log.info(logMgr.Info("开始检测遗器"))
        point = screenClientMgr.FindElement("./assets/static/images/fight/fight_reward.png", "image", 0.9, maxRetries=2)
        
        successRewardTopLeftX = point[0][0]
        successRewardTopLeftY = point[0][1]

        def CheckRelicsLoop():
            for i in range(2):
                for j in range(7):    
                    screenClientMgr.ClickElementWithPos(
                        (
                            (successRewardTopLeftX -380 + j *120, successRewardTopLeftY + 40 + i * 120),
                            (successRewardTopLeftX -380 + 120 + j *120, successRewardTopLeftY + 40 + 120 + i * 120)
                        )
                    )
                        
                    if not screenClientMgr.FindElement("./assets/static/images/fight/5star.png", "image", 0.9, maxRetries=1):
                        if screenClientMgr.ClickElement("./assets/static/images/fight/relics_info_close.png", "image", 0.9, maxRetries=3):
                            time.sleep(0.5)

                            # log.info(logMgr.Info(i))
                            # log.info(logMgr.Info(j))

                            if i == 1 and j == 6:
                                time.sleep(0.5)
                                screenClientMgr.MouseMove(successRewardTopLeftX, successRewardTopLeftY + 200)
                                screenClientMgr.MouseScroll(8, -1)
                                time.sleep(0.5)
                                CheckRelicsLoop()
                        else:
                            break
                    else:
                        time.sleep(0.5)
                        relicsName = screenClientMgr.GetSingleLineText(relicsNameCrop, blacklist=[], maxRetries=5)
                        relicsPart = screenClientMgr.GetSingleLineText(crop=(515.0 / 1920, 726.0 / 1080, 91.0 / 1920, 35.0 / 1080),blacklist=['+','0'], maxRetries=3)
                        log.info(logMgr.Info(f"{relicsName}:{relicsPart}"))
                        screenClientMgr.TakeScreenshot(crop=relicsPropCrop)
                        time.sleep(0.5)
                        
                        isProp = False
                        tempMainPropName = ''
                        propCount = -1
                        usefulPropCount = 0
                        relicsList = list()
                        isMainProp = True
                        result = ocrClientMgr.mOcr.RecognizeMultiLines(screenClientMgr.mDetect.screenshot)
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
                            # log.info(logMgr.Info(f"{tempListValue}")
                            relicsList.append(tempListValue)
                        
                        # log.info(logMgr.Info(f"{propCount}")
                        # log.info(logMgr.Info(f"{usefulPropCount}")
                        allPropText = '词条:'
                        for key in relicsList:
                            allPropText += f'{key},'
                        log.info(logMgr.Info(allPropText))
                        log.info(logMgr.Info(f"总词条数:{propCount},有效词条:{usefulPropCount}"))
                        BaseRelicsState.IsGoodRelics(relicsName, relicsPart, relicsList, propCount, usefulPropCount, tempMainPropName)
                        
                        time.sleep(0.5)
                        if screenClientMgr.ClickElement("./assets/static/images/fight/relics_info_close.png", "image", 0.9, maxRetries=3):
                            time.sleep(0.5)

                        log.info(logMgr.Info(i))
                        log.info(logMgr.Info(j))

                        if i == 1 and j == 6:
                            time.sleep(0.5)
                            screenClientMgr.MouseMove(successRewardTopLeftX, successRewardTopLeftY + 200)
                            screenClientMgr.MouseScroll(8, -1)
                            time.sleep(0.5)
                            CheckRelicsLoop()

        CheckRelicsLoop()

    @staticmethod
    def IsGoodRelics(relicsName, relicsPart, relicsList, propCount, usefulPropCount, mainPropName):
        log.info(logMgr.Info("开始检测遗器"))
        if (propCount >= 3 and usefulPropCount == 2):
            if relicsPart in ['头部', '手部']:
                log.warning(logMgr.Warning(f"发现头部/手部胚子"))
            elif relicsPart in '躯干':
                log.warning(logMgr.Warning(f"发现躯干胚子"))
            elif relicsPart in '脚部':
                log.warning(logMgr.Warning(f"发现脚部胚子"))
            elif relicsPart in '位面球':
                log.warning(logMgr.Warning(f"发现位面球胚子"))
            elif relicsPart in '连结绳':
                log.warning(logMgr.Warning(f"发现连结绳胚子"))

            BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)

        elif (propCount == 3 and usefulPropCount == 1):
            if relicsPart in ['头部', '手部']:
                log.warning(logMgr.Warning(f"发现头部/手部胚子"))
                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)

            elif relicsPart in '躯干' and mainPropName in ['暴击率','暴击伤害','攻击力']:
                log.warning(logMgr.Warning(f"发现躯干胚子"))
                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)

            elif relicsPart in '脚部' and mainPropName in ['速度','攻击力']:
                log.warning(logMgr.Warning(f"发现脚部胚子"))
                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)

            elif relicsPart in '位面球' and mainPropName in ['量子属性伤害加成','风属性伤害加成','火属性伤害加成','雷属性伤害加成','冰属性伤害加成','虚数属性伤害加成','攻击力']:
                log.warning(logMgr.Warning(f"发现位面球胚子"))
                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)

            elif relicsPart in '连结绳' and mainPropName not in ['防御力']:
                log.warning(logMgr.Warning(f"发现连结绳胚子"))
                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)
        elif (propCount == 3 and usefulPropCount == 0):
            if relicsPart in '躯干' and mainPropName in ['暴击率','暴击伤害']:
                log.warning(logMgr.Warning(f"发现躯干胚子"))
                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)
            else:
                BaseRelicsState.GarbageRelics()
        elif propCount == 4 and usefulPropCount == 0:
            BaseRelicsState.GarbageRelics()
        elif propCount == 4 and usefulPropCount == 2: # 主词条也会被算在有效词条中导致4词条的主词条双暴衣被标记胚子,副词条垃圾，为
            if relicsPart in '躯干' and mainPropName in ['暴击率','暴击伤害']:
                log.warning(logMgr.Warning(f"发现躯干胚子"))
                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsList)

    @staticmethod
    def CreateRelicsContent(relicsName, relicsPart, relicsList):
        log.info(logMgr.Info("正在生成胚子信息"))

        isMain = True
        subPropList = list()
        for prop in relicsList:
            if isMain:
                mainProp = prop
                isMain = False
            else:
                subPropList.append(prop)

        dataClientMgr.notifyContent["遗器胚子"].append({
            "遗器名称": relicsName,
            "遗器部位": relicsPart,
            "遗器主词条": mainProp,
            "遗器副词条": subPropList
        })

        time.sleep(1)
        if screenClientMgr.ClickElement("./assets/static/images/fight/relics_lock.png", "image", 0.9, maxRetries=5):
            log.info(logMgr.Info("胚子已锁定"))
            time.sleep(1)
        return
    
    @staticmethod
    def GarbageRelics():
        log.info(logMgr.Info("鉴定为垃圾"))
        if screenClientMgr.ClickElement("./assets/static/images/fight/relics_rubbish.png", "image", 0.9, maxRetries=5):
            log.info(logMgr.Info("已标记为垃圾"))
            time.sleep(1)
        return

    @staticmethod
    def SalvageRelicss():
        try:
            log.hr(logMgr.Hr("准备分解遗器"), 2)
            # screen.get_current_screen()
            if not configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_ENABLE][dataClientMgr.currentUid]:
                log.info(logMgr.Info("检测到分解遗器未开启,跳过分解遗器"))
                return
            screenClientMgr.ChangeTo('bag_relics')
            if screenClientMgr.ClickElement("分解", "text", maxRetries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                if screenClientMgr.ClickElement("分解", "text", maxRetries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                    time.sleep(1)
                    if screenClientMgr.ClickElement("./assets/static/images/relics/fast_select.png", "image", 0.9, maxRetries=10):
                        # 等待筛选界面弹出
                        time.sleep(1)
                        fastSelectCrop=(439.0 / 1920, 357.0 / 1080, 1018.0 / 1920, 448.0 / 1080)
                        screenClientMgr.ClickElement("全选已弃置", "text", maxRetries=10, crop=fastSelectCrop)
                        time.sleep(0.5)
                        screenClientMgr.ClickElement("3星及以下", "text", maxRetries=10, crop=fastSelectCrop)
                        time.sleep(0.5)
                        if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_4STAR_ENABLE][dataClientMgr.currentUid]:
                            screenClientMgr.ClickElement("4星及以下", "text", maxRetries=10, crop=fastSelectCrop)
                            time.sleep(0.5)
                        if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid]:
                            screenClientMgr.ClickElement("5星及以下", "text", maxRetries=10, crop=fastSelectCrop)
                            time.sleep(0.5)
                        if screenClientMgr.ClickElement("确认", "text", maxRetries=10, crop=fastSelectCrop):
                            time.sleep(3)
                            countText = screenClientMgr.GetSingleLineText((616.0 / 1920, 871.0 / 1080, 110.0 / 1920, 37.0 / 1080), [], 5)
                            count = countText.split('/')[0]
                            log.info(logMgr.Info(f"已选数量:{count}/500"))
                            time.sleep(0.5)
                            if count != 0:
                                if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid] and configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_TO_EXP][dataClientMgr.currentUid]:
                                    if screenClientMgr.ClickElement("./assets/static/images/relics/relics_exp.png", "image", 0.9, maxRetries=10):
                                        log.info(logMgr.Info("已点击将5星遗器分解为遗器经验材料"))
                                time.sleep(1)
                                if screenClientMgr.ClickElement("./assets/static/images/relics/salvage.png", "image", maxRetries=10):
                                    log.info(logMgr.Info(f"已点击分解遗器"))
                                    time.sleep(1)
                                    if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9, maxRetries=10):
                                        log.info(logMgr.Info(f"已点击确认"))
                                        time.sleep(1)
                                        if screenClientMgr.ClickElement("./assets/static/images/base/click_close.png", "image", 0.9, maxRetries=10):
                                            log.info(logMgr.Info(f"已点击关闭窗口"))
                                            time.sleep(1)
                                            log.info(logMgr.Info(f"分解遗器{count}件完成"))
                                            screenClientMgr.ChangeTo('main')
                                            return True
                            else:
                                log.error(logMgr.Error("分解遗器失败: 没有多余的遗器可供分解"))
                                screenClientMgr.ChangeTo('main')
                                return False
                log.error(logMgr.Error("分解遗器失败"))
                return False
        except Exception as e:
            log.error(logMgr.Error(f"分解遗器失败: {e}"))
            return False
        
    @staticmethod
    def DetectRelicsCount():
        try:
            log.hr(logMgr.Hr("准备检测遗器数量"), 2)
            # screen.get_current_screen()
            screenClientMgr.ChangeTo('bag_relics')
            relicsCountCrop = (1620.0 / 1920, 43.0 / 1080, 142.0 / 1920, 46.0 / 1080)
            relicsCountText = screenClientMgr.GetSingleLineText(relicsCountCrop, ['遗','器','数','量'], maxRetries=5)
            relicsCountText = relicsCountText.replace('量','')
            log.info(logMgr.Info(f"遗器数量:{relicsCountText}"))
            relicsCountText = relicsCountText.split('/')[0]
            dataClientMgr.currentRelicsCount = int(relicsCountText)
            
            dataClientMgr.notifyContent["遗器数量"] = dataClientMgr.currentRelicsCount
            if dataClientMgr.currentRelicsCount >= configMgr.mConfig[configMgr.mKey.RELICS_THRESHOLD_COUNT][dataClientMgr.currentUid]:
                log.warning(logMgr.Warning("检测到遗器数量超标"))
                if not BaseRelicsState.SalvageRelicss():
                    return BaseRelicsState.DetectRelicsCount()
                else:
                    return True
            else:
                return False

        except Exception as e:
            log.error(logMgr.Error(f"检测遗器数量失败: {e}"))
        return True
    
    @staticmethod
    def SalvageRelicss():
        try:
            log.hr(logMgr.Hr("准备分解遗器"), 2)
            # screen.get_current_screen()
            if not configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_ENABLE][dataClientMgr.currentUid]:
                log.info(logMgr.Info("检测到分解遗器未开启,跳过分解遗器"))
                return True
            screenClientMgr.ChangeTo('bag_relics')
            if screenClientMgr.ClickElement("分解", "text", maxRetries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                time.sleep(1)
                if screenClientMgr.ClickElement("./assets/static/images/relics/fast_select.png", "image", 0.9, maxRetries=10):
                    # 等待筛选界面弹出
                    time.sleep(1)
                    fast_select_crop=(439.0 / 1920, 357.0 / 1080, 1018.0 / 1920, 448.0 / 1080)
                    screenClientMgr.ClickElement("全选已弃置", "text", maxRetries=10, crop=fast_select_crop)
                    time.sleep(0.5)
                    screenClientMgr.ClickElement("3星及以下", "text", maxRetries=10, crop=fast_select_crop)
                    time.sleep(0.5)
                    if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_4STAR_ENABLE][dataClientMgr.currentUid]:
                        screenClientMgr.ClickElement("4星及以下", "text", maxRetries=10, crop=fast_select_crop)
                        time.sleep(0.5)
                    if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid]:
                        screenClientMgr.ClickElement("5星及以下", "text", maxRetries=10, crop=fast_select_crop)
                        time.sleep(0.5)
                    if screenClientMgr.ClickElement("确认", "text", maxRetries=10, crop=fast_select_crop):
                        time.sleep(3)
                        countText = screenClientMgr.GetSingleLineText((616.0 / 1920, 871.0 / 1080, 110.0 / 1920, 37.0 / 1080), [], 5)
                        count = countText.split('/')[0]
                        log.info(logMgr.Info(f"已选数量:{count}/500"))
                        time.sleep(0.5)
                        if count != 0:
                            if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid] and configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_TO_EXP][dataClientMgr.currentUid]:
                                if screenClientMgr.ClickElement("./assets/static/images/relics/relics_exp.png", "image", 0.9, maxRetries=10):
                                    log.info(logMgr.Info("已点击将5星遗器分解为遗器经验材料"))
                            time.sleep(1)
                            if screenClientMgr.ClickElement("./assets/static/images/relics/salvage.png", "image", maxRetries=10):
                                log.info(logMgr.Info(f"已点击分解遗器"))
                                time.sleep(1)
                                if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9, maxRetries=10):
                                    log.info(logMgr.Info(f"已点击确认"))
                                    time.sleep(1)
                                    if screenClientMgr.ClickElement("./assets/static/images/base/click_close.png", "image", 0.9, maxRetries=10):
                                        log.info(logMgr.Info(f"已点击关闭窗口"))
                                        time.sleep(1)
                                        log.info(logMgr.Info(f"分解遗器{count}件完成"))
                                        screenClientMgr.ChangeTo('main')
                                        return False
                        else:
                            log.error(logMgr.Error("分解遗器失败: 没有多余的遗器可供分解"))
                            screenClientMgr.ChangeTo('main')
                            return True
                log.error(logMgr.Error("分解遗器失败"))
                return True
        except Exception as e:
            log.error(logMgr.Error(f"分解遗器失败: {e}"))
            return True
        
    @staticmethod
    def SkipForRelicsCount():
        if dataClientMgr.currentRelicsCount >= configMgr.mConfig[configMgr.mKey.RELICS_THRESHOLD_COUNT][dataClientMgr.currentUid]:
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},检测到遗器数量超过{configMgr.mConfig[configMgr.mKey.RELICS_THRESHOLD_COUNT][dataClientMgr.currentUid]},所有可能获得遗器的副本全部跳过,出现该致命错误意味着你没有选择开启遗器自动分解开关,若不打算开启,则只能自行上号清理,否则每次上号时遗器数量超标时都会直接中止"))
            raise Exception(f"{nowtime},检测到遗器数量超过{configMgr.mConfig[configMgr.mKey.RELICS_THRESHOLD_COUNT][dataClientMgr.currentUid]},所有可能获得遗器的副本全部跳过,出现该致命错误意味着你没有选择开启遗器自动分解开关,若不打算开启,则只能自行上号清理,否则每次上号时遗器数量超标时都会直接中止")