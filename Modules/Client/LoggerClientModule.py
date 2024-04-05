from Modules.Common.LoggerBaseModule import LoggerBaseModule

class LoggerClientModule(LoggerBaseModule):

    def __new__(cls, level, loggerName, fileHandlerHead, formatter, coloredFormatter):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls, level, loggerName, fileHandlerHead, formatter, coloredFormatter)
        return cls.mInstance
    

