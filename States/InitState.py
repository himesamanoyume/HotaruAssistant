from States import *
from Hotaru.Client.ConfigClientHotaru import configClientMgr
from Modules.Utils.Data import Data
from Modules.Utils.Date import Date

class InitState(BaseState):

    mStateName = 'InitState'

    def OnBegin(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Begin Reload"))
        return False

    def OnRunning(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Running Reload"))
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.RELIC_SALVAGE_ENABLE, Data.tempUid, False)
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.RELIC_SALVAGE_4STAR_ENABLE, Data.tempUid, True)
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.RELIC_SALVAGE_5STAR_ENABLE, Data.tempUid, False)
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.RELIC_SALVAGE_5STAR_TO_EXP, Data.tempUid, False)
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.RELIC_THRESHOLD_COUNT, Data.tempUid, 1450)

        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.ECHO_OF_WAR_ENABLE, Data.tempUid, False)
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.ECHO_OF_WAR_TIMES, Data.tempUid, 0)

        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_FIN, Data.tempUid, False)

        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_NUMBER, Data.tempUid, 3)

        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_DIFFICULTY, Data.tempUid, 1)
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_FATE, Data.tempUid, '巡猎')
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_TEAM, Data.tempUid, {})
        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_SCORE, Data.tempUid, '0/1')

        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.LAST_RUN_TIMESTAMP, Data.tempUid)

        if Date.IsNext4AM(configClientMgr.mConfig[configClientMgr.mKey.LAST_RUN_TIMESTAMP][Data.tempUid], False):
            
            configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.DAILY_TASKS_SCORE, Data.tempUid, '0/1')
            configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.DAILY_TASKS_FIN, Data.tempUid, False)
            configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.DAILY_TASKS, Data.tempUid, {})

        configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_TIMESTAMP, Data.tempUid)

        if Date.IsNextMon4AM(configClientMgr.mConfig[configClientMgr.mKey.UNIVERSE_TIMESTAMP][Data.tempUid], False):
            maxScore = str(configClientMgr.mConfig[configClientMgr.mKey.UNIVERSE_SCORE][Data.tempUid]).split('/')[1]
            configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_SCORE, Data.tempUid, f"0/{maxScore}")
            configClientMgr.mConfigModule.DetectKeyIsExist(configClientMgr.mKey.UNIVERSE_FIN, Data.tempUid, False)

        return False

    def OnExit(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Exit Reload"))
        return False
