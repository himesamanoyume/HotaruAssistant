from datetime import datetime

class LoggerServerModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def Log(self, msg):
        pass
