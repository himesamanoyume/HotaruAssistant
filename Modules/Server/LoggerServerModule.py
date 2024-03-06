import datetime

class LoggerServerModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def Socket(cls, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]{msg}")

    @classmethod
    def Screen(cls, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}][SCREEN]|{msg}")
    
    @classmethod
    def Info(cls, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[92mINFO\033[0m|{msg}")

    @classmethod
    def Warning(cls, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[93mWARNING\033[0m|\033[93m{msg}\033[0m")

    @classmethod
    def Error(cls, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[91mERROR\033[0m|\033[91m{msg}\033[0m")
