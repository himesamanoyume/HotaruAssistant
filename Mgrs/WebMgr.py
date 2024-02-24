from Modules.Server.WebModule import WebModule

class WebMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mWebModule = WebModule()

        return cls.mInstance
