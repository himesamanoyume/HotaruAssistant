from datetime import datetime
import logging,os,glob,questionary
from colorama import init
from Modules.Utils.ColoredFormatter import ColoredFormatter
from Modules.Utils.TitleFormatter import TitleFormatter


class LoggerClientModule:

    mInstance = None

    def __new__(cls, level="INFO"):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mInstance.InitLogger(level)
        return cls.mInstance
    
    def InitLogger(self, level="INFO"):
        self.logger = logging.getLogger("HotaruAssistant")
        self.logger.propagate = False
        self.logger.setLevel(level)

        if not os.path.exists("logs"):
            os.makedirs("logs")

        self.ClearLog("./logs")
        
        file_handler = logging.FileHandler(f"./logs/{self.CurrentDatetime()}.log", encoding="utf-8")
        file_formatter = logging.Formatter('├ %(levelname)s|%(asctime)s|%(filename)s:%(lineno)d\n└ %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter('├ %(levelname)s|%(asctime)s|%(filename)s:%(lineno)d\n└ %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.hr = TitleFormatter.format_title

        return self.logger
    
    def CurrentDatetime(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def ClearLog(self, directory):
        files = glob.glob(directory + '/*')
        for f in files:
            if os.path.isfile(f):
                if os.path.getsize(f) <= 2048:
                    os.remove(f)

    def GetLogger(self):
        return self.logger
    
    def Info(self, msg, *args, **kwargs):
        self.GetLogger().info(msg, *args, **kwargs)

    def Error(self, msg, *args, **kwargs):
        self.GetLogger().error(msg, *args, **kwargs)

    def Warning(self, msg, *args, **kwargs):
        self.GetLogger().warning(msg, *args, **kwargs)

    def Hr(self, msg, *args, **kwargs):
        self.GetLogger().hr(msg, *args, **kwargs)

