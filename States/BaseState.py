from States import *

class BaseState(object):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseState'

    @classmethod
    def OnBegin(cls):
        logClientMgr.Info(f"{cls.mStateName} BaseBegin")

    @classmethod
    def OnRunning(cls):
        logClientMgr.Info(f"{cls.mStateName} BaseRunning")

    @classmethod
    def OnExit(cls):
        logClientMgr.Info(f"{cls.mStateName} BaseExit")
