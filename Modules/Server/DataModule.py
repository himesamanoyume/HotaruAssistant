class DataModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mUserDict = dict()
        return cls.mInstance
    
    @classmethod
    def LoadConfigToDict():
        pass
    
    @classmethod
    def SetData(cls, uid:str='-1', key:str='default', value=None):
        cls.mUserDict.update({uid:{key:value}})

    @classmethod
    def LoadAllCommonConfig(cls):
        cls.mUserDict.update()