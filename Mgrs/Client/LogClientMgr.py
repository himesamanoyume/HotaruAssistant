
from Modules.Client.LoggerClientModule import LoggerClientModule
from Hotaru.Client.SocketClientHotaru import socketClientMgr

class LogClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mLoggerModule = LoggerClientModule()
            cls.Hr("HotaruAssistant - Client\n启动!")
            cls.Info("Client日志已加载")

        return cls.mInstance
    
    @classmethod
    def Info(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        socketClientMgr.LogSendToServer("INFO", msg)
        cls.mLoggerModule.Info(msg, *args, **kwargs)

    @classmethod
    def Error(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        socketClientMgr.LogSendToServer("ERROR", msg)
        cls.mLoggerModule.Error(msg, *args, **kwargs)

    @classmethod
    def Warning(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        socketClientMgr.LogSendToServer("WARNING", msg)
        cls.mLoggerModule.Warning(msg, *args, **kwargs)

    @classmethod
    def Debug(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        cls.mLoggerModule.Debug(msg, *args, **kwargs)

    @classmethod
    def Hr(cls, msg, isLog = False, *args, **kwargs):
        if isLog:
            socketClientMgr.LogSendToServer("HR", msg)
        cls.mLoggerModule.Hr(msg, *args, **kwargs)



    
    
