
from Hotaru.Client.SocketClientHotaru import socketClientMgr

class LogClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            # cls.mLoggerModule = LoggerClientModule()
            cls.Hr("HotaruAssistant - Client\n启动!")
            cls.Info("Client日志已加载")

        return cls.mInstance
    
    @classmethod
    def Info(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        socketClientMgr.LogSendToServer("INFO", msg)
        return msg
        # cls.mLoggerModule.GetLogger().info(msg, *args, **kwargs)

    @classmethod
    def Error(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        socketClientMgr.LogSendToServer("ERROR", msg)
        return msg
        # cls.mLoggerModule.GetLogger().error(msg, *args, **kwargs)

    @classmethod
    def Warning(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        socketClientMgr.LogSendToServer("WARNING", msg)
        return msg
        # cls.mLoggerModule.GetLogger().warning(msg, *args, **kwargs)

    @classmethod
    def Screen(cls, msg):
        socketClientMgr.LogScreenSendToServer(msg)

    @classmethod
    def Debug(cls, msg, *args, **kwargs):
        msg = f"\033[91m[-1]\033[0m|临时流程|" + msg
        return msg
        # cls.mLoggerModule.GetLogger().debug(msg, *args, **kwargs)

    @classmethod
    def Hr(cls, msg, isLog = False, *args, **kwargs):
        if isLog:
            socketClientMgr.LogSendToServer("HR", msg)
        return msg
        # cls.mLoggerModule.GetLogger().hr(msg, *args, **kwargs)



    
    
