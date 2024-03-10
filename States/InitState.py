from States import *
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from Modules.Utils.Date import Date

class InitState(BaseState):

    mStateName = 'InitState'

    def OnBegin(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Begin Reload"))
        return False

    def OnRunning(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Running Reload"))
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_ENABLE, dataMgr.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_4STAR_ENABLE, dataMgr.tempUid, True)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_5STAR_ENABLE, dataMgr.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_5STAR_TO_EXP, dataMgr.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_THRESHOLD_COUNT, dataMgr.tempUid, 1450)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.ECHO_OF_WAR_ENABLE, dataMgr.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.ECHO_OF_WAR_TIMES, dataMgr.tempUid, 0)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FIN, dataMgr.tempUid, False)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_NUMBER, dataMgr.tempUid, 3)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_DIFFICULTY, dataMgr.tempUid, 1)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FATE, dataMgr.tempUid, '巡猎')
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_TEAM, dataMgr.tempUid, {})
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_SCORE, dataMgr.tempUid, '0/1')
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_BONUS_ENABLE, dataMgr.tempUid, False)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.LAST_RUN_TIMESTAMP, dataMgr.tempUid)

        if configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE] == {} or dataMgr.tempUid not in configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE].keys():
            configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.tempUid] = {}
            configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][dataMgr.tempUid].append('拟造花萼（金）')

        if configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES] == {} or dataMgr.tempUid not in configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES].keys():
            configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.tempUid] = {}
            configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.tempUid]['拟造花萼（金）'] = '雅利洛-回忆之蕾'
            configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.tempUid]['拟造花萼（赤）'] = '毁灭之蕾1'
            configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.tempUid]['凝滞虚影'] = '空海之形'
            configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.tempUid]['侵蚀隧洞'] = '睿治之径'
            configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.tempUid]['历战余响'] = '毁灭的开端'


        if Date.IsNext4AM(configMgr.mConfig[configMgr.mKey.LAST_RUN_TIMESTAMP][dataMgr.tempUid], False):
            
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS_SCORE, dataMgr.tempUid, 0)
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS_FIN, dataMgr.tempUid, False)
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS, dataMgr.tempUid, {})

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_TIMESTAMP, dataMgr.tempUid)

        if Date.IsNextMon4AM(configMgr.mConfig[configMgr.mKey.UNIVERSE_TIMESTAMP][dataMgr.tempUid], False):
            maxScore = str(configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][dataMgr.tempUid]).split('/')[1]
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_SCORE, dataMgr.tempUid, f"0/{maxScore}")
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FIN, dataMgr.tempUid, False)

        return False

    def OnExit(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Exit Reload"))
        return False
