from States import *
from .BaseFightState import BaseFightState
from .BaseRelicState import BaseRelicState

class DailyClearPowerState(BaseRelicState, BaseState):

    mStateName = 'DailyClearPowerState'

    def OnBegin(self):
        if configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0] == '模拟宇宙':
            return True
        else:
            instanceName = configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.currentUid][configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0]]

            instanceType = configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0]

            if instanceName == "无":
                log.info(logMgr.Info(f"跳过清体力,{configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0]}未开启"))
                return False
        
        BaseRelicState.DetectRelicCount()
        BaseRelicState.SkipForRelicCount()

        if dataMgr.currentPower <= 9:
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
        powerNeed = configMgr.mConfig[configMgr.mKey.POWER_NEEDS][configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.currentUid][0]]

        totalNumber = dataMgr.currentPower // powerNeed
        if totalNumber < 1:
            log.info(logMgr.Info(f"🟣开拓力 < {powerNeed}"))
            return False
        
        # if totalNumber is None:
        #     # number刷的次数
        #     totalNumber = dataMgr.currentPower // powerNeed
        #     if totalNumber < 1:
        #         log.info(logMgr.Info(f"🟣开拓力 < {powerNeed}"))
        #         return False
        # else:
        #     if powerNeed * totalNumber > dataMgr.currentPower:
        #         log.info(logMgr.Info(f"🟣开拓力 < {powerNeed}*{totalNumber}"))
        #         return False
        
        # Utils._temp += "<p>"+f'{instanceType} - {instanceName} - {number}次</p>'

        log.hr(logMgr.Hr(f"开始刷{instanceType} - {instanceName}，总计{totalNumber}次"), 2)
        BaseFightState.RunInstances(instanceType, instanceName, powerNeed, totalNumber)
        log.hr(logMgr.Hr("完成"), 2)

    def OnRunning(self):
        return False

    def OnExit(self):
        return False


