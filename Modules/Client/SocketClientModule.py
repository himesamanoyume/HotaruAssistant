from Modules.Common.SocketBaseModule import SocketBaseModule

class SocketClientModule(SocketBaseModule):
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
