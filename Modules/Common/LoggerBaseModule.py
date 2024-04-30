from datetime import datetime
import logging,os,glob
from Modules.Utils.ColoredFormatter import ColoredFormatter
from Modules.Utils.TitleFormatter import TitleFormatter


class LoggerBaseModule:

    mInstance = None

    def __new__(cls, level="INFO", loggerName = "HotaruAssistantBase", fileHandlerHead = 'base', formatter = '├ %(levelname)s | %(asctime)s | %(filename)s:%(lineno)d\n└ %(message)s', coloredFormatter = '├ %(levelname)s | %(asctime)s | %(filename)s:%(lineno)d\n└ %(message)s'):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mInstance.InitLogger(level, loggerName, fileHandlerHead, formatter, coloredFormatter)
            
        return cls.mInstance
    
    def InitLogger(self, level, loggerName, fileHandlerHead, formatter, coloredFormatter):
        self.logger = logging.getLogger(loggerName)
        self.logger.propagate = False
        self.logger.setLevel(level)

        if not os.path.exists("logs"):
            os.makedirs("logs")

        self.ClearLog("./logs", fileHandlerHead)
        
        file_handler = logging.FileHandler(f"./logs/{fileHandlerHead}-{self.CurrentDatetime()}.log", encoding="utf-8")
        file_formatter = logging.Formatter(formatter)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(coloredFormatter)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.hr = TitleFormatter.FormatTitle

        return self.logger
    
    def CurrentDatetime(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def ClearLog(self, directory, fileHandlerHead):
        files = glob.glob(directory + '/*')
        for f in files:
            if not fileHandlerHead in f:
                continue
            if os.path.isfile(f):
                if os.path.getsize(f) <= 2048:
                    os.remove(f)

    def GetLogger(self):
        return self.logger
