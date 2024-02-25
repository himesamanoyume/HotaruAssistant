from Modules.Client.ClickModule import ClickModule

class ClickMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mClickModule = ClickModule()

        return cls.mInstance
