
from Modules.Client.LoggerClientModule import LoggerClientModule

class LogClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mLoggerModule = LoggerClientModule()
            cls.Info("Client日志已加载")

        return cls.mInstance
    
    @classmethod
    def Info(cls, msg, *args, **kwargs):
        cls.mLoggerModule.Info(msg, *args, **kwargs)

    @classmethod
    def Error(cls, msg, *args, **kwargs):
        cls.mLoggerModule.Error(msg, *args, **kwargs)

    @classmethod
    def Warning(cls, msg, *args, **kwargs):
        cls.mLoggerModule.Warning(msg, *args, **kwargs)

    @classmethod
    def Hr(cls, msg, *args, **kwargs):
        cls.mLoggerModule.Hr(msg, *args, **kwargs)



    
    