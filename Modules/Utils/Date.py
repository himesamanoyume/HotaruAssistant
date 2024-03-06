from Hotaru.Client.LogClientHotaru import logClientMgr,log
from datetime import datetime, timedelta

class Date:
    @staticmethod
    def IsNext4AM(timestamp, isLog = True):
        dt_object = datetime.fromtimestamp(timestamp)
        current_time = datetime.now()
        if dt_object.hour < 4:
            next_4am = dt_object.replace(
                hour=4, minute=0, second=0, microsecond=0)
        else:
            next_4am = dt_object.replace(
                hour=4, minute=0, second=0, microsecond=0) + timedelta(days=1)
        if isLog:
            log.info(logClientMgr.Info(f"时间戳记录日期为{dt_object}"))
        if current_time >= next_4am:
            return True
        return False
    
    @staticmethod
    def IsNextMon4AM(timestamp, isLog = True):
        dt_object = datetime.fromtimestamp(timestamp)
        current_time = datetime.now()
        if dt_object.weekday() == 0 and dt_object.hour < 4:
            next_monday_4am = dt_object.replace(
                hour=4, minute=0, second=0, microsecond=0)
        else:
            days_until_next_monday = (
                7 - dt_object.weekday()) % 7 if dt_object.weekday() != 0 else 7
            next_monday_4am = dt_object.replace(
                hour=4, minute=0, second=0, microsecond=0) + timedelta(days=days_until_next_monday)
        if isLog:
            log.info(logClientMgr.Info(f"时间戳记录日期为{dt_object}"))
        if current_time >= next_monday_4am:
            return True
        return False

        
