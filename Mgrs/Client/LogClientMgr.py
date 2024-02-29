
from Modules.Client.LoggerClientModule import LoggerClientModule
from Hotaru.Client.SocketClientHotaru import socketClientMgr

class LogClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mLoggerModule = LoggerClientModule()
            cls.Hr("HotaruAssistant\n启动!")
            cls.Info("Client日志已加载")

        return cls.mInstance
    
    @classmethod
    def Info(cls, msg, *args, **kwargs):
        socketClientMgr.LogSendToServer(level='INFO' ,uid='-1', action='测试流程', msg=msg)
        cls.mLoggerModule.Info(msg, *args, **kwargs)

    @classmethod
    def Error(cls, msg, *args, **kwargs):
        socketClientMgr.LogSendToServer(level='Error' ,uid='-1', action='测试流程', msg=msg)
        cls.mLoggerModule.Error(msg, *args, **kwargs)

    @classmethod
    def Warning(cls, msg, *args, **kwargs):
        socketClientMgr.LogSendToServer(level='Warning' ,uid='-1', action='测试流程', msg=msg)
        cls.mLoggerModule.Warning(msg, *args, **kwargs)

    @classmethod
    def Hr(cls, msg, isLog = False, *args, **kwargs):
        if isLog:
            socketClientMgr.LogSendToServer(level='Hr' ,uid='-1', action='测试流程', msg=msg)
        cls.mLoggerModule.Hr(msg, *args, **kwargs)



    
    
