from States import *
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from Modules.Utils.Date import Date
from Modules.Utils.InitUidConfig import InitUidConfig
from Hotaru.Client.LogClientHotaru import logMgr, log

class InitState(BaseState):

    mStateName = 'InitState'

    def OnBegin(self):
        InitUidConfig.InitUidDefaultConfig(configMgr, logMgr, dataMgr.tempUid)

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
