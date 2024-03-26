from States import *
import time

class BaseNotifyState(BaseState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'BaseNotifyState'
    
    @staticmethod
    def SetNotifyContent():
        totalTime = time.time() - dataMgr.loopStartTimestamp
        if totalTime >= 3600:
            log.warning(logMgr.Warning(f"{dataMgr.currentUid}运行时长超时警告!"))
            # notify.announcement(f"{Utils.get_uid()}运行时长超时警告!","该UID运行总时长超60分钟,不健康,请立即检查优化", isSingle=True)
            
        _day = int(totalTime // 86400)
        _hour = int((totalTime - _day * 86400) // 3600)
        _minute = int(((totalTime - _day *86400) - _hour * 3600) // 60)
        _second = int(((totalTime - _day *86400) - _hour * 3600) - _minute * 60)
        dataMgr.notifyContent["上号时长"] = (f"{_day}天" if not _day == 0 else '') + (f"{_hour}小时" if not _hour == 0 else '') + (f"{_minute}分" if not _minute == 0 else '') + f"{_second}秒"
        log.info(logMgr.Info(f"本次运行时长:{dataMgr.notifyContent['上号时长']}"))
        