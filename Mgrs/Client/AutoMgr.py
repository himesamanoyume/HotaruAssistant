from Modules.Client.DetectScreenModule import DetectScreenModule
from Modules.Utils.Retry import Retry
from Hotaru.Client.LogClientHotaru import log,logMgr

class AutoMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance
    
    @staticmethod
    def RepeatAttempt(lambdaFunction, timeout = 10, repeatSleep = 0.5):
        return Retry.RepeatAttempt(lambdaFunction, timeout, repeatSleep)
