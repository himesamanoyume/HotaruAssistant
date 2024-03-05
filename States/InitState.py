from States import *
from Hotaru.Client.ConfigClientHotaru import configClientMgr
from Modules.Utils.ClientData import ClientData
from Modules.Utils.Date import Date

class InitState(BaseState):

    mStateName = 'InitState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} Begin Reload")
        return False

    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} Running Reload")
        configClientMgr.SetConfigValue(configClientMgr.mKey.RELIC_SALVAGE_ENABLE, ClientData.tempUid, False)
        configClientMgr.SetConfigValue(configClientMgr.mKey.RELIC_SALVAGE_4STAR_ENABLE, ClientData.tempUid, True)
        configClientMgr.SetConfigValue(configClientMgr.mKey.RELIC_SALVAGE_5STAR_ENABLE, ClientData.tempUid, False)
        configClientMgr.SetConfigValue(configClientMgr.mKey.RELIC_SALVAGE_5STAR_TO_EXP, ClientData.tempUid, False)
        configClientMgr.SetConfigValue(configClientMgr.mKey.RELIC_THRESHOLD_COUNT, ClientData.tempUid, 1450)

        configClientMgr.SetConfigValue(configClientMgr.mKey.ECHO_OF_WAR_ENABLE, ClientData.tempUid, False)
        configClientMgr.SetConfigValue(configClientMgr.mKey.ECHO_OF_WAR_TIMES, ClientData.tempUid, 0)

        configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_FIN, ClientData.tempUid, False)
        configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_NUMBER, ClientData.tempUid, 3)
        configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_DIFFICULTY, ClientData.tempUid, 1)
        configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_FATE, ClientData.tempUid, '巡猎')
        configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_TEAM, ClientData.tempUid, {})
        configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_SCORE, ClientData.tempUid, '0/1')

        if Date.IsNext4AM(configClientMgr.GetConfigValue(configClientMgr.mKey.LAST_RUN_TIMESTAMP, ClientData.tempUid), False):
            
            configClientMgr.SetConfigValue(configClientMgr.mKey.DAILY_TASKS_SCORE, ClientData.tempUid, '0/1')
            configClientMgr.SetConfigValue(configClientMgr.mKey.DAILY_TASKS_FIN, ClientData.tempUid, False)
            configClientMgr.SetConfigValue(configClientMgr.mKey.DAILY_TASKS, ClientData.tempUid, {})

        if Date.IsNextMon4AM(configClientMgr.GetConfigValue(configClientMgr.mKey.UNIVERSE_TIMESTAMP), False):
            maxScore = str(configClientMgr.GetConfigValue(configClientMgr.mKey.UNIVERSE_SCORE, ClientData.tempUid)).split('/')[1]
            configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_SCORE, ClientData.tempUid, f"0/{maxScore}")
            configClientMgr.SetConfigValue(configClientMgr.mKey.UNIVERSE_FIN, ClientData.tempUid, False)

        return False

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} Exit Reload")
        return False
