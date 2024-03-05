from States import *

class BaseState(object):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseState'

    def OnBegin(self):
        logClientMgr.Info(f"{self.mStateName} BaseBegin")
        return False

    def OnRunning(self):
        logClientMgr.Info(f"{self.mStateName} BaseRunning")
        return False

    def OnExit(self):
        logClientMgr.Info(f"{self.mStateName} BaseExit")
        return False
