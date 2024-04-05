from States.Client import *
from Modules.Utils.InitUidConfig import InitUidConfig

class InitState(BaseClientState):

    mStateName = 'InitState'

    def OnBegin(self):
        InitUidConfig.InitUidDefaultConfig(configMgr, log, logMgr, dataClientMgr.tempUid)

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
