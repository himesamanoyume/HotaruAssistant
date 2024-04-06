from States.Client import *

class ToolsInitAccountState(BaseClientState):

    mStateName = 'ToolsInitAccountState'

    def OnBegin(self):
        uidCrop = (70.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080)
        try:
            dataClientMgr.currentUid = screenClientMgr.GetSingleLineText(crop=uidCrop, blacklist=[], maxRetries=9)
            if dataClientMgr.currentUid == None:
                nowtime = time.time()
                log.error(logMgr.Error(f"未能读取到UID"))
                raise Exception(f"未能读取到UID")
            dataClientMgr.loopStartTimestamp = time.time()
            log.info(logMgr.Info(f"识别到UID为:{dataClientMgr.currentUid}"))
        except Exception as e:
            nowtime = time.time()
            log.error(logMgr.Error(f"{nowtime},识别UID失败: {e}"))
            raise Exception(f"{nowtime},识别UID失败: {e}")

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    