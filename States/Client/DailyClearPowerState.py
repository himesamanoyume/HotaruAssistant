from States.Client import *
from .BaseFightState import BaseFightState

class DailyClearPowerState(BaseFightState, BaseClientState):

    mStateName = 'DailyClearPowerState'

    def OnBegin(self):
        instanceName = configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataClientMgr.currentUid][configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataClientMgr.currentUid][0]]

        instanceType = configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataClientMgr.currentUid][0]

        if instanceName == "无":
            log.info(logMgr.Info(f"跳过清体力,{configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataClientMgr.currentUid][0]}未开启"))
            return True
            
        self.DetectRelicsCount()
        self.SkipForRelicsCount()

        if dataClientMgr.currentPower <= 9:
            log.info(logMgr.Info(f"跳过清体力,体力太低"))
            return True
     
        log.hr(logMgr.Hr("开始清体力"), 0)

        # 兼容旧设置
        if "·" in instanceName:
            instanceName = instanceName.split("·")[0]
        
        if instanceName == "无":
            log.warning(logMgr.Warning(f"{instanceType}未开启"))
            return False
        log.hr(logMgr.Hr(f"准备{instanceType}"), 2)
        powerNeed = configMgr.mConfig[configMgr.mKey.POWER_NEEDS][configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataClientMgr.currentUid][0]]

        totalNumber = dataClientMgr.currentPower // powerNeed
        if instanceType in ['饰品提取']:
            totalNumber = totalNumber + dataClientMgr.currentImmersifiers
            
        if totalNumber < 1:
            log.info(logMgr.Info(f"🟣开拓力 < {powerNeed}"))
            return True
        
        log.hr(logMgr.Hr(f"开始刷{instanceType} - {instanceName}，总计{totalNumber}次"), 2)
        self.RunInstances(instanceType, instanceName, powerNeed, totalNumber)
        log.hr(logMgr.Hr("完成"), 2)
        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False


