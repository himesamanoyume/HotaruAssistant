from Hotaru.Client.LogClientHotaru import log,logMgr
import time

class Retry:
    @staticmethod
    def RepeatAttempt(lambdaFunction, timeout = 10, repeatSleep = 0.5):
        startTime = time.time()
        while time.time() - startTime < timeout:
            try:
                result = lambdaFunction()
                if result:
                    return result
            except Exception as e:
                log.error(logMgr.Error(e))
                    
            time.sleep(repeatSleep)
        
        return False