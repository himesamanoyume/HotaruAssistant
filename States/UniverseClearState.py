from States import *
from .BaseUniverseState import BaseUniverseState
from Modules.Utils.Command import Command

class UniverseClearState(BaseUniverseState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'UniverseClearState'

    def OnBegin(self):
        screenMgr.ChangeTo('main')

        log.info(logMgr.Info("开始校准"))
        if Command.SubprocessWithTimeout([configMgr.mConfig[configMgr.mKey.PYTHON_EXE_PATH], "align_angle.py"], 60, configMgr.mConfig[configMgr.mKey.UNIVERSE_PATH], configMgr.env):
            
            screenMgr.ChangeTo('guide3')
            log.info(logMgr.Info("开始模拟宇宙"))
        else:
            log.error(logMgr.Error("校准失败"))
            return True

    def OnRunning(self):
        return self.RunUniverse() 

    def OnExit(self):
        return False
    
    def RunUniverse(self):
        command = [configMgr.mConfig[configMgr.mKey.PYTHON_EXE_PATH], "states.py"]
        time.sleep(0.5)
        if not dataMgr.currentUniverseScore < dataMgr.maxCurrentUniverseScore:
            if (configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0] == '模拟宇宙' and dataMgr.currentImmersifiers < 4):
                log.info(logMgr.Info("鉴定为沉浸器数量不足,跳过"))
                return True
          
        time.sleep(0.5)

        if configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0] == '模拟宇宙' or not configMgr.mConfig[configMgr.mKey.UNIVERSE_FIN][dataMgr.currentUid]:
            
            self.SelectUniverse()
            if dataMgr.currentUniverseScore == 0:
                log.info(logMgr.Info("积分为0,鉴定为首次进行模拟宇宙"))
                if dataMgr.currentImmersifiers > 0:
                    command.append("--bonus=1")
            elif dataMgr.currentUniverseScore == dataMgr.maxCurrentUniverseScore:
                log.info(logMgr.Info("积分为最大积分,鉴定为完成周常后额外进行模拟宇宙"))
                if dataMgr.currentImmersifiers > 0:
                    command.append("--bonus=1")
                if not configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0] == '模拟宇宙':
                    log.info(logMgr.Info("鉴定为正在每日任务中,最大积分且清体力不为模拟宇宙的情况下将直接跳过"))
                    return False
            else:
                log.info(logMgr.Info("积分不为0也不为最大积分,鉴定为不是首次进行模拟宇宙"))
                command.append("--bonus=1")
            
            command.append(f"--nums=1")
                
            # end
            log.info(logMgr.Info("将开始进行模拟宇宙"))
            command.append(f"--fate={configMgr.mConfig[configMgr.mKey.UNIVERSE_FATE][dataMgr.currentUid]}")
            if Command.SubprocessWithTimeout(command, configMgr.mConfig[configMgr.mKey.UNIVERSE_TIMEOUT] * 3600, configMgr.mConfig[configMgr.mKey.UNIVERSE_PATH], configMgr.env):
            
                screenMgr.ChangeTo('main')
                # 此时保存运行的时间戳
                configMgr.SaveTimestampByUid(configMgr.mKey.UNIVERSE_TIMESTAMP, dataMgr.currentUid)
                # end

                if configMgr.mConfig[configMgr.mKey.UNIVERSE_BONUS_ENABLE][dataMgr.currentUid]:
                    # 此时领取积分奖励
                    self.GetUniverseReward()
                    # end

                self.RunUniverse()

                log.info(logMgr.Info("🎉模拟宇宙已完成1次🎉"))
                dataMgr.notifyContent["副本情况"]["模拟宇宙"] += 1
                return False
            else:
                log.error(logMgr.Error("模拟宇宙失败"))
                return True
            # end
    
    def SelectUniverse(self):
        time.sleep(1)

        # 传送
        instance_name_crop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
        screenMgr.ClickElement("./assets/images/screen/guide/power.png", "image", maxRetries=10)
        Flag = False
        match configMgr.mConfig[configMgr.mKey.UNIVERSE_NUMBER][dataMgr.currentUid]:
            case 3:
                worldNumber = '第三世界'
            case 4:
                worldNumber = '第四世界'
            case 5:
                worldNumber = '第五世界'
            case 6:
                worldNumber = '第六世界'
            case 7:
                worldNumber = '第七世界'
            case 8:
                worldNumber = '第八世界'
            case _:
                worldNumber = '第三世界'
                # Utils._content['universe_number'] = f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'><p>模拟宇宙难度选择有误,请告知我检查配置</p></blockquote>"

        for i in range(5):
            if screenMgr.ClickElement("传送", "min_distance_text", crop=instance_name_crop, include=True, source=worldNumber, sourceType="text"):
                Flag = True
                break
            screenMgr.MouseScroll(20, -1)
            # 等待界面完全停止
            time.sleep(1)
        if not Flag:
            log.error(logMgr.Error("⚠️刷副本未完成 - 没有找到指定副本名称⚠️"))
            return True

        time.sleep(3)
        
        # 选择难度,0不是难度
        d = configMgr.mConfig[configMgr.mKey.UNIVERSE_DIFFICULTY][dataMgr.currentUid]
        if not d in [1,2,3,4,5]:
            log.warning(logMgr.Warning("难度设置不合法,进行难度5"))
            d = 5
        if configMgr.mConfig[configMgr.mKey.UNIVERSE_NUMBER][dataMgr.currentUid] in [5,6,7,8] and d > 4:
            log.warning(logMgr.Warning("第五、第六、第七、第八世界暂不支持难度4以上,进行难度4"))
            d = 4
        
        # 用嵌套函数
        self.SelectUniverseDifficulty(d)

        time.sleep(1)

        if screenMgr.ClickElement("./assets/images/screen/universe/download_char.png", "image", 0.9,maxRetries=10):
            time.sleep(1)
            self.ClearTeam(1)

            charCount = 0
            screenMgr.ClickElementWithPos(((70, 300),(70, 300)), action="move")
            for character in configMgr.mConfig[configMgr.mKey.UNIVERSE_TEAM][dataMgr.currentUid]:
                time.sleep(0.5)
                if charCount == 4:
                    break
                log.info(logMgr.Info(f"{character}"))
                if not screenMgr.ClickElement(f"./assets/images/character/{character}.png","image", 0.85, maxRetries=10, takeScreenshot=True):
                    time.sleep(0.5)
                    screenMgr.MouseScroll(30, -1)
                    if not screenMgr.ClickElement(f"./assets/images/character/{character}.png", "image", 0.85, maxRetries=10, takeScreenshot=True):
                        time.sleep(0.5)
                        screenMgr.MouseScroll(30, 1)
                        continue
                    else:
                        log.info(logMgr.Info("该角色已选中"))
                        screenMgr.MouseScroll(30, 1)
                        charCount+=1
                else:
                    log.info(logMgr.Info("该角色已选中"))
                    charCount += 1
                time.sleep(0.5)
            if charCount == 4:
                return False
            else:
                log.error(logMgr.Error(f"{nowtime}模拟宇宙未能选中4位配置中的角色,请检查"))
                raise Exception(f"{nowtime}模拟宇宙未能选中4位配置中的角色,请检查")
        else:
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime}模拟宇宙未找到下载角色按钮"))
            raise Exception(f"{nowtime}模拟宇宙未找到下载角色按钮")
        
    def SelectUniverseDifficulty(self, d):
        difficultyCrop=(85.0 / 1920, 108.0 / 1080, 94.0 / 1920, 836.0 / 1080)
        if d==0:
            log.error(logMgr.Error(f"难度{d}不合法"))
            return

        if not screenMgr.ClickElement(f"./assets/images/universe/on_{d}.png","image", 0.9, maxRetries=5, crop=difficultyCrop):
                log.info(logMgr.Info(f"未选中难度{d},尝试选择难度{d}"))
                time.sleep(0.5)
                if screenMgr.ClickElement(f"./assets/images/universe/off_{d}.png","image", 0.9, maxRetries=5, crop=difficultyCrop):
                    log.info(logMgr.Info(f"检查是否选中难度{d}"))
                    time.sleep(0.5)
                    # 此处尝试无识别直接点击难度位置
                    # screenMgr.ClickElement_with_pos(((135, 160+(d-1)*110),(135, 160+(d-1)*110)))
                    if screenMgr.ClickElement(f"./assets/images/universe/on_{d}.png","image", 0.9, maxRetries=5, crop=difficultyCrop):
                        time.sleep(0.5)
                        if screenMgr.FindElement("./assets/images/screen/universe/download_char.png", "image", 0.9, maxRetries=10):
                            time.sleep(0.5)
                            log.info(logMgr.Info(f"已选中难度{d}"))
                            return
                        else:
                            time.sleep(0.5)
                            log.warning(logMgr.Warning(f"已选中难度{d},但该难度未解锁,嵌套进入难度{d-1}"))
                            self.SelectUniverseDifficulty(d-1)
                            return
                    else:
                        log.warning(logMgr.Warning(f"可能该难度未开放,嵌套进入难度{d-1}"))
                        self.SelectUniverseDifficulty(d-1)
                        return
                else:
                    log.warning(logMgr.Warning(f"可能该难度未开放,嵌套进入难度{d-1}"))
                    self.SelectUniverseDifficulty(d-1)
                    return
        else:
            if not screenMgr.FindElement("./assets/images/screen/universe/download_char.png", "image", 0.9, maxRetries=10):
                time.sleep(0.5)
                log.warning(logMgr.Warning(f"已选中难度{d},但该难度未解锁,嵌套进入难度{d-1}"))
                self.SelectUniverseDifficulty(d-1)
            else:
                time.sleep(0.5)
                log.info(logMgr.Info(f"已选中难度{d}"))
                return
    
    def ClearTeam(self, j):
        if j == 10:
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},模拟宇宙清理队伍失败"))
            raise Exception(f"{nowtime},模拟宇宙清理队伍失败")
        
        for i in range(4):
            screenMgr.ClickElementWithPos(((663+i*105, 837),(663+i*105, 837)))
            time.sleep(1)
        if screenMgr.FindElement("./assets/images/universe/all_clear_team.png", "image", 0.95, takeScreenshot=True):
            log.info(logMgr.Info("队伍已清空"))
            return
        else:
            self.ClearTeam(j+1)