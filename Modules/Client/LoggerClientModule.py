from datetime import datetime

class LoggerClientModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    
    def Info(self, msg, *args, **kwargs):
        self.GetLogger().info(msg, *args, **kwargs)

    def Error(self, msg, *args, **kwargs):
        self.GetLogger().error(msg, *args, **kwargs)

    def Warning(self, msg, *args, **kwargs):
        self.GetLogger().warning(msg, *args, **kwargs)

    def Hr(self, msg, *args, **kwargs):
        self.GetLogger().hr(msg, *args, **kwargs)
