from .ConfigKeySubModule import ConfigKeySubModule

class BaseConfigModule(object):

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mKey = ConfigKeySubModule()
        return cls.mInstance
    
    