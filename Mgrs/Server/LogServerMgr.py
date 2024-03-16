
from Modules.Server.LoggerServerModule import LoggerServerModule

class LogServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mLoggerServerModule = LoggerServerModule()
            cls.Info("Server日志已加载")

        return cls.mInstance
    
    @classmethod
    def Info(cls, msg):
        cls.mLoggerServerModule.Info(msg)

    @classmethod
    def Warning(cls, msg):
        cls.mLoggerServerModule.Warning(msg)

    @classmethod
    def Error(cls, msg):
        cls.mLoggerServerModule.Error(msg)

    @classmethod
    def Debug(cls, msg):
        cls.mLoggerServerModule.Debug(msg)

    @classmethod
    def Socket(cls, msg):
        cls.mLoggerServerModule.Socket(msg)

    @classmethod 
    def Hr(cls, msg, level=0):
        cls.mLoggerServerModule.Hr(msg, level)




    
    
