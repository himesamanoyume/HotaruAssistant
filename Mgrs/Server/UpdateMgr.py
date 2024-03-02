
from Modules.Server.UpdateModule import UpdateModule

class UpdateMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mUpdate = UpdateModule()

        return cls.mInstance
        