from States import *
from Hotaru.Client.ScreenHotaru import screenMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from Modules.Utils.Retry import Retry
from Hotaru.Client.LogClientHotaru import log,logMgr
import time

class InitAccountState(BaseState):

    mStateName = 'InitAccountState'

    def OnBegin(self):
        uidCrop = (70.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080)
        try:
            dataMgr.currentUid = screenMgr.GetSingleLineText(crop=uidCrop, blacklist=[], maxRetries=9)
            if dataMgr.currentUid == None:
                nowtime = time.time()
                log.error(logMgr.Error(f"未能读取到UID"))
                raise Exception(f"未能读取到UID")
            dataMgr.loopStartTimestamp = time.time()
            log.info(logMgr.Info(f"识别到UID为:{dataMgr.currentUid}"))
            configMgr.mConfig.SetValue(configMgr.mKey.LAST_RUNNING_UID, dataMgr.currentUid)
        except Exception as e:
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},识别UID失败: {e}"))
            raise Exception(f"{nowtime},识别UID失败: {e}")

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
