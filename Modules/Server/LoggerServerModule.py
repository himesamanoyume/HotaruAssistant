from datetime import datetime

class LoggerServerModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def Info(cls, msg):
        print(msg)

    @classmethod
    def Error(cls, msg):
        print(f"\033[91m{msg}\033[0m")
