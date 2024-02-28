from .ConfigKeySubModule import ConfigKeySubModule

class BaseConfigModule(object):

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            
            cls.mConfigKey = ConfigKeySubModule()
        return cls.mInstance
    
    