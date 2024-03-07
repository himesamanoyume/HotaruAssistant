import time

class Retry:
    def RepeatAttempt(log, lambdaFunction, timeout = 10, repeatSleep = 0.5, logMgr = None):
        startTime = time.time()

        while time.time() - startTime < timeout:
            try:
                result = lambdaFunction()
                if result:
                    return result
            except Exception as e:
                log.error(e)
                if logMgr:
                    logMgr.Error(e)
            
            time.sleep(repeatSleep)
        
        return False