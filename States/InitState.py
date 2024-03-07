from States import *
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import data
from Modules.Utils.Date import Date

class InitState(BaseState):

    mStateName = 'InitState'

    def OnBegin(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Begin Reload"))
        return False

    def OnRunning(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Running Reload"))
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_ENABLE, data.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_4STAR_ENABLE, data.tempUid, True)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_5STAR_ENABLE, data.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_SALVAGE_5STAR_TO_EXP, data.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.RELIC_THRESHOLD_COUNT, data.tempUid, 1450)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.ECHO_OF_WAR_ENABLE, data.tempUid, False)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.ECHO_OF_WAR_TIMES, data.tempUid, 0)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FIN, data.tempUid, False)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_NUMBER, data.tempUid, 3)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_DIFFICULTY, data.tempUid, 1)
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FATE, data.tempUid, '巡猎')
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_TEAM, data.tempUid, {})
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_SCORE, data.tempUid, '0/1')
        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_BONUS_ENABLE, data.tempUid, False)

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.LAST_RUN_TIMESTAMP, data.tempUid)

        if Date.IsNext4AM(configMgr.mConfig[configMgr.mKey.LAST_RUN_TIMESTAMP][data.tempUid], False):
            
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS_SCORE, data.tempUid, '0/1')
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS_FIN, data.tempUid, False)
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS, data.tempUid, {})

        configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_TIMESTAMP, data.tempUid)

        if Date.IsNextMon4AM(configMgr.mConfig[configMgr.mKey.UNIVERSE_TIMESTAMP][data.tempUid], False):
            maxScore = str(configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][data.tempUid]).split('/')[1]
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_SCORE, data.tempUid, f"0/{maxScore}")
            configMgr.mConfigModule.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FIN, data.tempUid, False)

        return False

    def OnExit(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Exit Reload"))
        return False
