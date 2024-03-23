from Hotaru.Client.LogClientHotaru import log,logMgr
import time,threading

class Retry:
    @staticmethod
    def ReThread(lambdaFunction, timeout = 10, repeatSleep = 1, *args, **kwargs):
        t = threading.Thread(target=Retry.Re(lambdaFunction, timeout, repeatSleep, *args, **kwargs))
        t.start()
        
    @staticmethod
    def Re(lambdaFunction, timeout = 10, repeatSleep = 1, *args, **kwargs):
        startTime = time.time()
        while time.time() - startTime < timeout:
            try:
                # log.debug(logMgr.Debug(f"正在调用Re:{lambdaFunction}"))
                result = lambdaFunction(*args, **kwargs)
                if result:
                    return result
            except Exception as e:
                log.error(logMgr.Error(f"重试报错: {e}"))
                    
            time.sleep(repeatSleep)
        
        return False