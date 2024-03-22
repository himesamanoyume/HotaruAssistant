import random,time
from datetime import datetime, timedelta

class Date:
    @staticmethod
    def IsNext4AM(timestamp, isLog = True):
        dtObject = datetime.fromtimestamp(timestamp)
        current_time = datetime.now()
        if dtObject.hour < 4:
            next_4am = dtObject.replace(
                hour=4, minute=0, second=0, microsecond=0)
        else:
            next_4am = dtObject.replace(
                hour=4, minute=0, second=0, microsecond=0) + timedelta(days=1)
        # if isLog:
            # log.info(logMgr.Info(f"时间戳记录日期为{dt_object}"))
        if current_time >= next_4am:
            return True
        return False
    
    @staticmethod
    def IsNextMon4AM(timestamp, isLog = True):
        dtObject = datetime.fromtimestamp(timestamp)
        current_time = datetime.now()
        if dtObject.weekday() == 0 and dtObject.hour < 4:
            next_monday_4am = dtObject.replace(
                hour=4, minute=0, second=0, microsecond=0)
        else:
            days_until_next_monday = (
                7 - dtObject.weekday()) % 7 if dtObject.weekday() != 0 else 7
            next_monday_4am = dtObject.replace(
                hour=4, minute=0, second=0, microsecond=0) + timedelta(days=days_until_next_monday)
        # if isLog:
        #     log.info(logMgr.Info(f"时间戳记录日期为{dt_object}"))
        if current_time >= next_monday_4am:
            return True
        return False
    
    @staticmethod
    def GetTimeNext4am():
        now = datetime.now()
        next_4am = now.replace(hour=4, minute=0, second=0, microsecond=0)

        if now >= next_4am:
            next_4am += timedelta(days=1)

        time_until_next_4am = next_4am - now
        return int(time_until_next_4am.total_seconds())
    
    @staticmethod
    def GetWaitTimeWithTotalTime(configMgr):
        waitTime = configMgr.mConfig[configMgr.mKey.NEXT_LOOP_TIME] * 3600
        # 距离第二天凌晨4点剩余秒数，+30避免显示3点59分不美观，#7
        waitTimeNextDay = Date.GetTimeNext4am() + random.randint(30, 600)
        # 取最小值
        waitTime = min(waitTime, waitTimeNextDay)
        return waitTime
    
    @staticmethod
    def CalculateFutureTime(seconds):
        currentTime = datetime.now()
        futureTime = currentTime + timedelta(seconds=seconds)
        if futureTime.date() == currentTime.date():
            return f"今天{futureTime.hour}时{futureTime.minute}分"
        elif futureTime.date() == currentTime.date() + timedelta(days=1):
            return f"明天{futureTime.hour}时{futureTime.minute}分"
        else:
            return "输入秒数不合法"

        
