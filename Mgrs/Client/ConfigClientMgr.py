
from Modules.Utils.ConfigKey import ConfigKey
from Modules.Common.ConfigModule import ConfigModule
import time

class ConfigClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigModule()
            cls.mKey = ConfigKey()

        return cls.mInstance
    
    def SaveTimestampByUid(self, key, uid):
        if key == {}:
            self.mConfig[key][uid] = 0
            self.mConfig[key][uid] = time.time()
        else:
            self.mConfig[key][uid] = time.time()
        
        return True
    