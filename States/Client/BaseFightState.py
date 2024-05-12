from States.Client import *
from .BaseRelicsState import BaseRelicsState
import math

class BaseFightState(BaseRelicsState, BaseClientState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseFightState'

    @staticmethod
    def AlwaysWaitFight(instanceName):
        screenClientMgr.PressKey("w")
        if screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/fight/fight_again.png", "image", 0.9):
            log.info(logMgr.Info("检测到战斗结束"))
            return True
        
        screenClientMgr.PressKey("w")
        if screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/fight/fight_fail.png", "image", 0.9):
            log.info(logMgr.Info("检测到战斗失败/重试"))
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战败"))
            raise Exception(f"{nowtime},挑战{instanceName}时战败")
        
        screenClientMgr.PressKey("w")
        if not screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/base/2x_speed_on.png", "image", 0.9, crop=(1618.0 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
            log.info(logMgr.Info("尝试开启二倍速"))
            screenClientMgr.PressKey("b")

        screenClientMgr.PressKey("w")
        if not screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/base/2x_speed_on.png", "image", 0.9, crop=(1719.0 / 1920, 51.0 / 1080, 84.0 / 1920, 22.0 / 1080)):
            log.info(logMgr.Info("尝试开启自动战斗"))
            screenClientMgr.PressKey("v")

    @staticmethod
    def EnableWaitFight(instanceName):
        time.sleep(5)
        for i in range(20):
            if not screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/base/2x_speed_on.png", "image", 0.9, crop=(1618.0 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
                log.info(logMgr.Info("尝试开启二倍速"))
                screenClientMgr.PressKey("b")
            else:
                log.info(logMgr.Info("二倍速已开启"))
                break

        time.sleep(5)
        for i in range(20):
            if not screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/base/2x_speed_on.png", "image", 0.9, crop=(1719.0 / 1920, 51.0 / 1080, 84.0 / 1920, 22.0 / 1080)):
                log.info(logMgr.Info("尝试开启自动战斗"))
                screenClientMgr.PressKey("v")
            else:
                log.info(logMgr.Info("自动战斗已开启"))
                break

        log.info(logMgr.Info("等待战斗"))

        return Retry.Re(lambda: BaseFightState.CheckFight(instanceName), 600)

    @staticmethod
    def CheckFight(instanceName):
        if screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/fight/fight_again.png", "image", 0.9):
            log.info(logMgr.Info("检测到战斗结束"))
            return True
        
        if screenClientMgr.FindElementWithShowMultiArea("./assets/static/images/fight/fight_fail.png", "image", 0.9):
            log.info(logMgr.Info("检测到战斗失败/重试"))
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战败"))
            raise Exception(f"{nowtime},挑战{instanceName}时战败")

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

        screenClientMgr.ChangeTo('guide3')
        instanceTypeCrop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        if not screenClientMgr.ClickElement(instanceType, "text", crop=instanceTypeCrop):
            if screenClientMgr.ClickElement("侵蚀隧洞", "text", maxRetries=10, crop=instanceTypeCrop):
                screenClientMgr.MouseScroll(12, -1)
                time.sleep(0.5)
                screenClientMgr.ClickElement(instanceType, "text", crop=instanceTypeCrop)
        # 截图过快会导致结果不可信
        time.sleep(1)
        # 传送
        instanceNameCrop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
        screenClientMgr.ClickElement("./assets/static/images/screen/guide/power.png", "image", maxRetries=10)
        Flag = False
        instanceMapType = ''

        if instanceType in ['拟造花萼（赤）']:
            source = f"./assets/static/{dataClientMgr.meta['拟造花萼（赤）'][instanceName][1]}"
            for i in range(math.ceil(len(dataClientMgr.meta[instanceType]) / 3)):
                if screenClientMgr.ClickElement("进入", "min_distance_text", crop=instanceNameCrop, include=True, source=source,  sourceType="image"):
                    log.info("该副本限时开放中,但你并没有解锁该副本")
                    Flag = True
                    break
                elif screenClientMgr.ClickElement("追踪", "min_distance_text", crop=instanceNameCrop, include=True, source=source,  sourceType="image"):
                    nowtime = time.time()
                    log.error(logMgr.Error(f"{nowtime},{instanceName}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                    raise Exception(f"{nowtime},{instanceName}:你似乎没有解锁这个副本?总之无法传送到该副本")
                elif screenClientMgr.ClickElement("传送", "min_distance_text", crop=instanceNameCrop, include=True, source=source,  sourceType="image"):
                    Flag = True
                    break
                else:
                    screenClientMgr.MouseScroll(18, -1)
                    # 等待界面完全停止
                    time.sleep(1)
        elif instanceType in ['拟造花萼（金）']:
            instanceMap, instanceMapType = instanceName.split('-')
            instance_map_name = dataClientMgr.meta['星球'][instanceMap]

            for i in range(math.ceil((len(dataClientMgr.meta[instanceType]) / 3) / 3)):
                if screenClientMgr.ClickElement(f"./assets/static/images/screen/guide/{instance_map_name}_on.png", "image", 0.9, maxRetries=10) or screenClientMgr.ClickElement(f"./assets/static/images/screen/guide/{instance_map_name}_off.png", "image", 0.9, maxRetries=10):
                    if screenClientMgr.ClickElement("传送", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceMapType):
                        Flag = True
                        break
                    elif screenClientMgr.ClickElement("进入", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceMapType, sourceType="text"):
                        log.info("该副本限时开放中,但你并没有解锁该副本")
                        Flag = True
                        break
                    elif screenClientMgr.ClickElement("追踪", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceMapType, sourceType="text"):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},{instanceMapType}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                        raise Exception(f"{nowtime},{instanceMapType}:你似乎没有解锁这个副本?总之无法传送到该副本")
                else:
                    # 等待界面完全停止
                    time.sleep(1)     
        else:
            for i in range(math.ceil(len(dataClientMgr.meta[instanceType]) / 3)):
                if screenClientMgr.ClickElement("传送", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceName, sourceType="text"):
                    Flag = True
                    break
                elif screenClientMgr.ClickElement("进入", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceName, sourceType="text"):
                    log.info("该副本限时开放中,但你并没有解锁该副本")
                    Flag = True
                    break
                elif screenClientMgr.ClickElement("追踪", "min_distance_text", crop=instanceNameCrop, include=True, source=instanceName, sourceType="text"):
                    nowtime = time.time()
                    log.error(logMgr.Error(f"{nowtime},{instanceName}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                    raise Exception(f"{nowtime},{instanceName}:你似乎没有解锁这个副本?总之无法传送到该副本")
                else:
                    screenClientMgr.MouseScroll(18, -1)
                    # 等待界面完全停止
                    time.sleep(1)
        
        if not Flag:
            log.error(logMgr.Error("⚠️刷副本未完成 - 没有找到指定副本名称⚠️"))
            return True
        
        # 验证传送是否成功
        time.sleep(5)
        if not screenClientMgr.FindElement(instanceName.replace("1", "").replace("2", "").replace("3", "").replace("4", ""), "text", maxRetries=5, include=True, crop=(1172.0 / 1920, 5.0 / 1080, 742.0 / 1920, 636.0 / 1080)):
            if not screenClientMgr.FindElement(instanceMapType, "text", maxRetries=10, include=True, crop=(1172.0 / 1920, 5.0 / 1080, 742.0 / 1920, 636.0 / 1080)):
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
            result = screenClientMgr.FindElement("./assets/static/images/screen/guide/plus.png", "image", 0.9, maxRetries=10,
                                    crop=(1174.0 / 1920, 775.0 / 1080, 738.0 / 1920, 174.0 / 1080))
            if fullCount == 0:
                for i in range(incomplete_count - 1):
                    screenClientMgr.ClickElementWithPos(result)
                    time.sleep(0.5)
            else:
                for i in range(5):
                    screenClientMgr.ClickElementWithPos(result)
                    time.sleep(0.5)
        if screenClientMgr.ClickElement("挑战", "text", maxRetries=10, needOcr=True):
            if instanceType == "历战余响":
                time.sleep(1)
                screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9)
            if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataClientMgr.currentUid] == False:
                BaseClientState.BorrowCharacter()

            if configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_ENABLE][dataClientMgr.currentUid]:
                if configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][dataClientMgr.currentUid][instanceType] == 0:
                    if configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][dataClientMgr.currentUid]['默认配队'] == 0:
                        log.info(logMgr.Info(f"不进行切换配队"))
                    else:
                        BaseClientState.ChangeTeam(configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][dataClientMgr.currentUid]['默认配队'])
                else:
                    BaseClientState.ChangeTeam(configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][dataClientMgr.currentUid][instanceType])
            
            if screenClientMgr.ClickElement("开始挑战", "text", maxRetries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                time.sleep(1)
                if screenClientMgr.FindElement("./assets/static/images/fight/no_power.png", "image", 0.9):
                    nowtime = time.time()
                    log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时开拓力不足,但却触发了挑战,请检查"))
                    raise Exception(f"{nowtime},挑战{instanceName}时开拓力不足,但却触发了挑战,请检查")
                
                elif screenClientMgr.FindElement("./assets/static/images/fight/char_dead.png", "image", 0.9):
                    nowtime = time.time()
                    log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时有角色处于无法战斗的状态,请检查"))
                    raise Exception(f"{nowtime},挑战{instanceName}时有角色处于无法战斗的状态,请检查")
                
                if instanceType in ["凝滞虚影", "侵蚀隧洞", "历战余响"]:
                    time.sleep(2)
                    if instanceType in ["凝滞虚影"]:
                        for i in range(3):
                            screenClientMgr.PressMouse()
                            time.sleep(3)
                    for i in range(totalCount - 1):

                        if configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'ALWAYS':
                            if Retry.Re(lambda: BaseFightState.AlwaysWaitFight(instanceName), 600, 30):
                                log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(1)"))
                            else:
                                nowtime = time.time()
                                log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                                raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")
                            
                        elif configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'ENABLE':
                            if BaseFightState.EnableWaitFight(instanceName):
                                log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(1)"))
                            else:
                                nowtime = time.time()
                                log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                                raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")
                            
                        elif configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'DISABLE':
                            if Retry.Re(lambda: BaseFightState.CheckFight(instanceName), 600):
                                log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(1)"))
                            else:
                                nowtime = time.time()
                                log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                                raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")


                        if instanceType == "侵蚀隧洞":
                            BaseRelicsState.InstanceGetRelics()
                        time.sleep(1)
                        screenClientMgr.ClickElement("./assets/static/images/fight/fight_again.png", "image", 0.9, maxRetries=5)
                        # if instanceType == "历战余响":
                        #     time.sleep(1)
                        #     screenMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9, maxRetries=5) 
                        time.sleep(1) 
                else:
                    if fullCount > 0:
                        for i in range(fullCount - 1):
                            if configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'ALWAYS':
                                if Retry.Re(lambda: BaseFightState.AlwaysWaitFight(instanceName), 600, 30):
                                    log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(2)"))
                                else:
                                    nowtime = time.time()
                                    log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                                    raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")
                                
                            elif configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'ENABLE':
                                if BaseFightState.EnableWaitFight(instanceName):
                                    log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(2)"))
                                else:
                                    nowtime = time.time()
                                    log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                                    raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")
                                
                            elif configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'DISABLE':
                                if Retry.Re(lambda: BaseFightState.CheckFight(instanceName), 600):
                                    log.info(logMgr.Info(f"第{i+1}次{instanceType}副本完成(2)"))
                                else:
                                    nowtime = time.time()
                                    log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                                    raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")
                                
                            if not (fullCount == 1 and incomplete_count == 0):
                                screenClientMgr.ClickElement("./assets/static/images/fight/fight_again.png", "image", 0.9, maxRetries=10)
                
                # 这是最后一次战斗在循环之外的等待战斗
                if configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'ALWAYS':
                    if not Retry.Re(lambda: BaseFightState.AlwaysWaitFight(instanceName), 600, 30):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                        raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")
                    
                elif configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'ENABLE':
                    if not BaseFightState.EnableWaitFight(instanceName):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                        raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")
                    
                elif configMgr.mConfig[configMgr.mKey.ALWAYS_DETECT_FIGHT_STATUS] == 'DISABLE':
                    if not Retry.Re(lambda: BaseFightState.CheckFight(instanceName), 600):
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},挑战{instanceName}时战斗超时"))
                        raise Exception(f"{nowtime},挑战{instanceName}时战斗超时")

                if instanceType == "侵蚀隧洞":
                    BaseRelicsState.InstanceGetRelics()

                if fullCount > 0:
                    log.info(logMgr.Info(f"{fullCount*6}次{instanceType}副本完成(3)"))
                    dataClientMgr.notifyContent["副本情况"][instanceType] += fullCount*6
                elif instanceType == "凝滞虚影" or "侵蚀隧洞" :
                    log.info(logMgr.Info(f"{totalCount}次{instanceType}副本完成(4)"))
                    dataClientMgr.notifyContent["副本情况"][instanceType] += totalCount
                else:
                    log.info(logMgr.Info(f"{incomplete_count}次{instanceType}副本完成(5)"))
                    dataClientMgr.notifyContent["副本情况"][instanceType] += incomplete_count
                # 速度太快，点击按钮无效
                time.sleep(1)
                screenClientMgr.ClickElement("./assets/static/images/fight/fight_exit.png", "image", 0.9, maxRetries=10)
                time.sleep(2)
                if fullCount > 0 and incomplete_count > 0:
                    BaseFightState.RunInstances(instanceType, instanceName, aTimesNeedPower, incomplete_count)
                else:
                    log.info(logMgr.Info("副本任务完成"))
                    return True
