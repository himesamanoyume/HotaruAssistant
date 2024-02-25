
from Modules.Server.LoggerServerModule import LoggerServerModule

class LogServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mLoggerModule = LoggerServerModule()

        return cls.mInstance
    
    @classmethod
    def Log(cls, msg):
        cls.mLoggerModule.Log(msg)




    
    
