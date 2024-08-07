from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import dataClientMgr
from Hotaru.Client.SocketClientHotaru import socketClientMgr

class LogClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.Hr("HotaruAssistant - Client\n启动!")
            cls.Info("Client日志已加载")

        return cls.mInstance
    
    @staticmethod
    def Info(msg, *args, **kwargs):
        msg = f"[{dataClientMgr.currentUid}] | {dataClientMgr.currentState} | {msg}"
        socketClientMgr.LogSendToServer("INFO", msg)
        return msg

    @staticmethod
    def Error(msg, *args, **kwargs):
        msg = f"[{dataClientMgr.currentUid}] | {dataClientMgr.currentState} | {msg}"
        socketClientMgr.LogSendToServer("ERROR", msg)
        return msg

    @staticmethod
    def Warning(msg, *args, **kwargs):
        msg = f"[{dataClientMgr.currentUid}] | {dataClientMgr.currentState} | {msg}"
        socketClientMgr.LogSendToServer("WARNING", msg)
        return msg

    @staticmethod
    def Heart():
        socketClientMgr.LogHeartSendToServer()

    @staticmethod
    def Debug(msg, *args, **kwargs):
        msg = f"[{dataClientMgr.currentUid}] | {dataClientMgr.currentState} | {msg}"
        if configMgr.mConfig[configMgr.mKey.LOG_LEVEL] == "DEBUG":
            socketClientMgr.LogSendToServer("DEBUG", msg)
        return msg

    @staticmethod
    def Hr(msg, isLog = False, *args, **kwargs):
        if isLog:
            socketClientMgr.LogSendToServer("HR", msg)
        return msg



    
    
