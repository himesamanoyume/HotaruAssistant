
from Modules.Json.JsonModule import JsonModule

class JsonMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mJsonModule = JsonModule()

        return cls.mInstance