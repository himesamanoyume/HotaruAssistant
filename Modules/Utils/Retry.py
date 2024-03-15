from Hotaru.Client.LogClientHotaru import log,logMgr
import time

class Retry:
    @staticmethod
    def Re(lambdaFunction, timeout = 10, repeatSleep = 0.5, *args, **kwargs):
        startTime = time.time()
        print("start")
        while time.time() - startTime < timeout:
            try:
                print(lambdaFunction)
                result = lambdaFunction(*args, **kwargs)
                print("end")
                if result:
                    return result
            except Exception as e:
                log.error(logMgr.Error(f"重试报错: {e}"))
                    
            time.sleep(repeatSleep)
        
        return False