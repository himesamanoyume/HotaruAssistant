from States import *
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from Modules.Utils.Date import Date
from Modules.Utils.InitUidConfig import InitUidConfig
from Hotaru.Client.LogClientHotaru import logMgr, log

class InitState(BaseState):

    mStateName = 'InitState'

    def OnBegin(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Begin Reload"))
        return False

    def OnRunning(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Running Reload"))
        InitUidConfig.InitUidDefaultConfig(configMgr, logMgr, dataMgr.tempUid)
        return False

    def OnExit(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Exit Reload"))
        return False
