from Hotaru.Updater.ConfigUpdaterHotaru import configMgr
# configMgr必须最前

from Modules.Common.LoggerBaseModule import LoggerBaseModule
log = LoggerBaseModule(
    configMgr.mConfig[configMgr.mKey.LOG_LEVEL], 
    "HotaruAssistantUpdater",
    'updater'
).GetLogger()