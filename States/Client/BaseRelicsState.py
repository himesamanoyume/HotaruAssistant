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

        if dataClientMgr.currentImmersifiers > 0:
            dataClientMgr.currentImmersifiers = dataClientMgr.currentImmersifiers - 1
            if dataClientMgr.currentImmersifiers < 0:
                dataClientMgr.currentImmersifiers = 0
                
        point = screenClientMgr.FindElement("./assets/static/images/fight/fight_reward.png", "image", 0.9)
        
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

                    if not screenClientMgr.FindElement("./assets/static/images/fight/relics_info_close.png", "image", 0.9):
                        screenClientMgr.ClickElementWithPos(
                            (
                                (successRewardTopLeftX -380 + j *120, successRewardTopLeftY + 40 + i * 120),
                                (successRewardTopLeftX -380 + 120 + j *120, successRewardTopLeftY + 40 + 120 + i * 120)
                            )
                        )
                        
                    if not screenClientMgr.FindElement("./assets/static/images/fight/5star.png", "image", 0.9, maxRetries=2):
                        if screenClientMgr.ClickElement("./assets/static/images/fight/relics_info_close.png", "image", 0.9):
                            time.sleep(0.5)
                            if i == 1 and j == 6:
                                time.sleep(0.5)
                                screenClientMgr.MouseMove(successRewardTopLeftX, successRewardTopLeftY + 200)
                                screenClientMgr.MouseScroll(8, -1)
                                time.sleep(0.5)
                                CheckRelicsLoop()
                        else:
                            break
                    else:
                        relicsName = screenClientMgr.GetSingleLineText(relicsNameCrop, blacklist=[])
                        relicsPart = screenClientMgr.GetSingleLineText(crop=(515.0 / 1920, 726.0 / 1080, 91.0 / 1920, 35.0 / 1080),blacklist=['+','0'])
                        log.info(logMgr.Info(f"{relicsName}:{relicsPart}"))
                        screenClientMgr.TakeScreenshot(crop=relicsPropCrop)
                        
                        isProp = False
                        tempMainPropName = ''
                        propCount = -1
                        usefulPropCount = 0
                        relicsPropList = list()
                        isMainProp = True
                        result = ocrClientMgr.mOcr.RecognizeMultiLines(screenClientMgr.mDetect.screenshot)
                        tempListValue = ''
                        for box in result:
                            text = box[1][0]
                            if text in ['暴击率','暴击伤害','生命值','攻击力','防御力','能量恢复效率','效果命中','效果抵抗','速度','击破特攻','治疗量加成','量子属性伤害提高','风属性伤害提高','火属性伤害提高','雷属性伤害提高','冰属性伤害提高','虚数属性伤害提高', '物理属性伤害提高']:
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

                                tempListValue += f'{text}'
                                isProp = False
                                propCount += 1
                            else:
                                continue
                            relicsPropList.append(tempListValue)
                        
                        log.info(logMgr.Info(relicsPropList))
                        allPropText = '属性:'
                        for key in relicsPropList:
                            allPropText += f'{key},'
                        log.info(logMgr.Info(allPropText))
                        log.info(logMgr.Info(f"总属性数:{propCount},有效属性:{usefulPropCount}"))
                        BaseRelicsState.IsGoodRelics(relicsName, relicsPart, relicsPropList, propCount, usefulPropCount, tempMainPropName)
                        
                        if screenClientMgr.FindElement("./assets/static/images/fight/relics_info_close.png", "image", 0.9):
                            screenClientMgr.ClickElement("./assets/static/images/fight/relics_info_close.png", "image", 0.9)
                            time.sleep(1)

                        if i == 1 and j == 6:
                            time.sleep(0.5)
                            screenClientMgr.MouseMove(successRewardTopLeftX, successRewardTopLeftY + 200)
                            screenClientMgr.MouseScroll(8, -1)
                            time.sleep(0.5)
                            CheckRelicsLoop()

        CheckRelicsLoop()
    
    @staticmethod
    def IsGoodRelics(relicsName, relicsPart, relicsPropList, propCount, usefulPropCount, mainPropName):
        log.info(logMgr.Info("开始检测遗器"))
        relicsSubPropList = relicsPropList.copy()
        del relicsSubPropList[0]
        processed = False

        def FindRelicsSet(relicsName):
            for keyword, relicsSetName in dataClientMgr.meta['隧洞遗器'].items():
                if keyword in relicsName:
                    return relicsSetName
                
            for keyword2, relicsSetName2 in dataClientMgr.meta['位面饰品'].items():
                if keyword2 in relicsName:
                    return relicsSetName2
                
            return None

        if len(configMgr.mConfig[configMgr.mKey.RELICS_FILTER][dataClientMgr.currentUid]) > 0:
            log.info(logMgr.Info("开始运作自定义遗器筛选器规则"))

            relicsSetName = FindRelicsSet(relicsName)
            suitable = False
            if relicsSetName:
                log.debug(logMgr.Debug(f"发现对应套装遗器:{relicsSetName}"))
                for filter in configMgr.mConfig[configMgr.mKey.RELICS_FILTER][dataClientMgr.currentUid]:
                    if relicsSetName in filter['遗器套装'] and relicsPart == filter['遗器部位'] and mainPropName == filter['目标主属性'] and propCount == filter['匹配副属性数量']:

                        log.info(logMgr.Info(f"发现匹配成功的筛选器规则"))
                        targetUsefulSubPropCount = 0
                        log.debug(logMgr.Debug(f"当前副属性列表:{relicsSubPropList}"))

                        for targetSubPropName in filter['目标副属性']:
                            log.debug(logMgr.Debug(f"正在匹配副属性:{targetSubPropName}"))
                            for subPropName in relicsSubPropList:
                                if targetSubPropName in subPropName:
                                    targetUsefulSubPropCount += 1
                                
                        if targetUsefulSubPropCount == len(filter['目标副属性']) and filter['匹配副属性数量'] == len(relicsSubPropList):
                            suitable = True
                        else:
                            log.warning(logMgr.Warning(f"该遗器不符合自定义筛选器的要求(1)"))

                        if suitable:
                            if filter['处理方式'] == '弃置':
                                BaseRelicsState.GarbageRelics()
                                processed = True
                            else:
                                log.warning(logMgr.Warning(f"发现{relicsPart}胚子"))
                                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)
                                processed = True
                        else:
                            log.warning(logMgr.Warning(f"该遗器不符合自定义筛选器的要求(2)"))

                        break
                    else:
                        log.debug(logMgr.Debug(f"未发现匹配的筛选器规则"))
            else:
                log.error(logMgr.Error(f"未找到对应的遗器套装"))
        
        if not processed:
            log.info(logMgr.Info("开始运作遗器默认筛选规则"))
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

                BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)

            elif (propCount == 3 and usefulPropCount == 1):
                if relicsPart in ['头部', '手部']:
                    log.warning(logMgr.Warning(f"发现头部/手部胚子"))
                    BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)

                elif relicsPart in '躯干' and mainPropName in ['暴击率','暴击伤害','攻击力']:
                    log.warning(logMgr.Warning(f"发现躯干胚子"))
                    BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)

                elif relicsPart in '脚部' and mainPropName in ['速度','攻击力']:
                    log.warning(logMgr.Warning(f"发现脚部胚子"))
                    BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)

                elif relicsPart in '位面球' and mainPropName in ['量子属性伤害提高','风属性伤害提高','火属性伤害提高','雷属性伤害提高','冰属性伤害提高','虚数属性伤害提高','攻击力']:
                    log.warning(logMgr.Warning(f"发现位面球胚子"))
                    BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)

                elif relicsPart in '连结绳' and mainPropName not in ['防御力']:
                    log.warning(logMgr.Warning(f"发现连结绳胚子"))
                    BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)
            elif (propCount == 3 and usefulPropCount == 0):
                if relicsPart in '躯干' and mainPropName in ['暴击率','暴击伤害']:
                    log.warning(logMgr.Warning(f"发现躯干胚子"))
                    BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)
                else:
                    BaseRelicsState.GarbageRelics()
            elif propCount == 4 and usefulPropCount == 0:
                BaseRelicsState.GarbageRelics()
            elif propCount == 4 and usefulPropCount == 2: # 主属性也会被算在有效属性中导致4属性的主属性双暴衣被标记胚子,副属性垃圾，为
                if relicsPart in '躯干' and mainPropName in ['暴击率','暴击伤害']:
                    log.warning(logMgr.Warning(f"发现躯干胚子"))
                    BaseRelicsState.CreateRelicsContent(relicsName, relicsPart, relicsPropList)
        else:
            log.info(logMgr.Info(f"由于已被自定义筛选器处理过, 因此跳过默认筛选器处理"))

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
            "遗器主属性": mainProp,
            "遗器副属性": subPropList
        })

        if screenClientMgr.ClickElement("./assets/static/images/fight/relics_lock.png", "image", 0.9):
            log.info(logMgr.Info("胚子已锁定"))
        return
    
    @staticmethod
    def GarbageRelics():
        log.info(logMgr.Info("鉴定为垃圾"))
        if screenClientMgr.ClickElement("./assets/static/images/fight/relics_rubbish.png", "image", 0.9):
            log.info(logMgr.Info("已标记为垃圾"))
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
            if screenClientMgr.ClickElement("分解", "text", crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                if screenClientMgr.ClickElement("分解", "text", crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                    if screenClientMgr.ClickElement("./assets/static/images/relics/fast_select.png", "image", 0.9):
                        # 等待筛选界面弹出
                        fastSelectCrop=(439.0 / 1920, 357.0 / 1080, 1018.0 / 1920, 448.0 / 1080)
                        screenClientMgr.ClickElement("全选已弃置", "text", crop=fastSelectCrop)
                        screenClientMgr.ClickElement("3星及以下", "text", crop=fastSelectCrop)
                        if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_4STAR_ENABLE][dataClientMgr.currentUid]:
                            screenClientMgr.ClickElement("4星及以下", "text", crop=fastSelectCrop)
                        if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid]:
                            screenClientMgr.ClickElement("5星及以下", "text", crop=fastSelectCrop)
                        if screenClientMgr.ClickElement("确认", "text", crop=fastSelectCrop):
                            countText = screenClientMgr.GetSingleLineText((616.0 / 1920, 871.0 / 1080, 110.0 / 1920, 37.0 / 1080), [])
                            count = countText.split('/')[0]
                            log.info(logMgr.Info(f"已选数量:{count}/500"))
                            if count != 0:
                                if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid] and configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_TO_EXP][dataClientMgr.currentUid]:
                                    if screenClientMgr.ClickElement("./assets/static/images/relics/relics_exp.png", "image", 0.9):
                                        log.info(logMgr.Info("已点击将5星遗器分解为遗器经验材料"))
                                if screenClientMgr.ClickElement("./assets/static/images/relics/salvage.png", "image"):
                                    log.info(logMgr.Info(f"已点击分解遗器"))
                                    if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                                        log.info(logMgr.Info(f"已点击确认"))
                                        if screenClientMgr.ClickElement("./assets/static/images/base/click_close.png", "image", 0.9):
                                            log.info(logMgr.Info(f"已点击关闭窗口"))
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
            relicsCountText = screenClientMgr.GetSingleLineText(relicsCountCrop, ['遗','器','数','量'])
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
            if not configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_ENABLE][dataClientMgr.currentUid]:
                log.info(logMgr.Info("检测到分解遗器未开启,跳过分解遗器"))
                return True
            screenClientMgr.ChangeTo('bag_relics')
            if screenClientMgr.ClickElement("分解", "text", crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                if screenClientMgr.ClickElement("./assets/static/images/relics/fast_select.png", "image", 0.9):
                    # 等待筛选界面弹出
                    fastSelectCrop=(439.0 / 1920, 357.0 / 1080, 1018.0 / 1920, 448.0 / 1080)
                    screenClientMgr.ClickElement("全选已弃置", "text", crop=fastSelectCrop)
                    screenClientMgr.ClickElement("3星及以下", "text", crop=fastSelectCrop)
                    if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_4STAR_ENABLE][dataClientMgr.currentUid]:
                        screenClientMgr.ClickElement("4星及以下", "text", crop=fastSelectCrop)
                    if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid]:
                        screenClientMgr.ClickElement("5星及以下", "text", crop=fastSelectCrop)
                    if screenClientMgr.ClickElement("确认", "text", crop=fastSelectCrop):
                        countText = screenClientMgr.GetSingleLineText((616.0 / 1920, 871.0 / 1080, 110.0 / 1920, 37.0 / 1080), [], 5)
                        count = countText.split('/')[0]
                        log.info(logMgr.Info(f"已选数量:{count}/500"))
                        if count != 0:
                            if configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE][dataClientMgr.currentUid] and configMgr.mConfig[configMgr.mKey.RELICS_SALVAGE_5STAR_TO_EXP][dataClientMgr.currentUid]:
                                if screenClientMgr.ClickElement("./assets/static/images/relics/relics_exp.png", "image", 0.9):
                                    log.info(logMgr.Info("已点击将5星遗器分解为遗器经验材料"))
                            if screenClientMgr.ClickElement("./assets/static/images/relics/salvage.png", "image"):
                                log.info(logMgr.Info(f"已点击分解遗器"))
                                if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                                    log.info(logMgr.Info(f"已点击确认"))
                                    if screenClientMgr.ClickElement("./assets/static/images/base/click_close.png", "image", 0.9):
                                        log.info(logMgr.Info(f"已点击关闭窗口"))
                                        log.info(logMgr.Info(f"分解遗器{count}件完成"))
                                        screenClientMgr.ChangeTo('main')
                                        return False
                        else:
                            log.error(logMgr.Error("分解遗器失败: 没有多余的遗器可供分解"))
                            screenClientMgr.ChangeTo('main')
                            return True
                log.error(logMgr.Error("分解遗器失败。可能的原因1:分解遗器品级只勾选到4星及以下时已无任何可选遗器，这将出现未选中任何遗器因此无法分解任何遗器"))
                return True
        except Exception as e:
            log.error(logMgr.Error(f"分解遗器失败: {e}"))
            return True
        
    @staticmethod
    def SkipForRelicsCount():
        if dataClientMgr.currentRelicsCount >= configMgr.mConfig[configMgr.mKey.RELICS_THRESHOLD_COUNT][dataClientMgr.currentUid]:
            BaseClientState.ThrowException(f"检测到遗器数量超过{configMgr.mConfig[configMgr.mKey.RELICS_THRESHOLD_COUNT][dataClientMgr.currentUid]},所有可能获得遗器的副本全部跳过,出现该致命错误意味着你没有选择开启遗器自动分解开关,若不打算开启,则只能自行上号清理,否则每次上号时遗器数量超标时都会直接中止")