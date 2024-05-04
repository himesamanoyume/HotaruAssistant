from Hotaru.Client.LogClientHotaru import logMgr,log
from Mgrs.Base.ScreenBaseMgr import ScreenBaseMgr
import time


class ScreenClientMgr(ScreenBaseMgr):
    
    @staticmethod
    def NeedLoginError():
        nowtime = time.time()
        log.error(logMgr.Error(f"{nowtime},检测到需要登录,可能是注册表不正确或已更改了密码"))
        raise Exception(f"{nowtime},检测到需要登录,可能是注册表不正确或已更改了密码")
    
    @staticmethod
    def RelicsFullError():
        nowtime = time.time()
        log.error(logMgr.Error(f"{nowtime},检测到背包遗器已满,本次运行已中断,如有需要请在配置中开启自动分解遗器选项,或手动上号清理并保持空位富余"))
        raise Exception(f"{nowtime},检测到背包遗器已满,本次运行已中断,如有需要请在配置中开启自动分解遗器选项,或手动上号清理并保持空位富余")
