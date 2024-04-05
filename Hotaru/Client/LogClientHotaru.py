from Hotaru.Client.ConfigClientHotaru import configMgr
# configMgr必须最前
from Mgrs.Client.LogClientMgr import LogClientMgr
logMgr = LogClientMgr()

from Modules.Common.LoggerBaseModule import LoggerBaseModule
log = LoggerBaseModule(
    configMgr.mConfig[configMgr.mKey.LOG_LEVEL], 
    "HotaruAssistantClient",
    'client'
).GetLogger()