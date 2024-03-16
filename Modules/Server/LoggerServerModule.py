import datetime
from Modules.Utils.TitleFormatter import TitleFormatter

class LoggerServerModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def Socket(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]{msg}")
    
    def Info(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[92mINFO\033[0m|{msg}")

    def Warning(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[93mWARNING\033[0m|\033[93m{msg}\033[0m")

    def Error(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[91mERROR\033[0m|\033[91m{msg}\033[0m")

    def Debug(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[94mDEBUG\033[0m|\033[94m{msg}\033[0m")

    def Hr(self, msg, level=0):
        TitleFormatter.FormatTitle(msg, level)
