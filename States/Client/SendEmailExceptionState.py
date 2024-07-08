from States.Client import *
from .BaseNotifyState import BaseNotifyState
from Hotaru.Client.NotifyHotaru import notifyMgr
import os

class SendEmailExceptionState(BaseNotifyState):

    mStateName = 'SendEmailExceptionState'

    def OnBegin(self):
        if configMgr.mConfig[configMgr.mKey.NOTIFY_SMTP_ENABLE]:
            self.SetNotifyContent()

            time.sleep(3)
            if os.path.exists(f'./screenshots/{dataClientMgr.currentUid}/excepetion.png'):
                img = f"<img loading='lazy' src='cid:exceptionImg'>"
            else:
                img = f"<p>未检测到异常状态截图</p>"
            
            content = f"<span class=important style=background-color:#40405f;color:#66ccff>{dataClientMgr.tempText}</span>{img}"
            
            if dataClientMgr.currentAction == "每日任务流程":
                if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataClientMgr.currentUid]:
                    notifyMgr.SendNotifySingle(
                        title=f"每日异常,UID:{dataClientMgr.currentUid}", 
                        subTitle=f"异常状态/{dataClientMgr.currentAction}", 
                        content=content, 
                        configMgr=configMgr, 
                        dataMgr=dataClientMgr, 
                        uid=dataClientMgr.currentUid
                        )
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
                else:
                    notifyMgr.SendNotifySingle(
                        title=f"每日异常,UID:{dataClientMgr.currentUid}", 
                        subTitle=f"异常状态/{dataClientMgr.currentAction}", 
                        content=content, 
                        configMgr=configMgr, 
                        dataMgr=dataClientMgr, 
                        uid=dataClientMgr.currentUid
                        )
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
            elif dataClientMgr.currentAction == "差分宇宙流程":
                notifyMgr.SendNotifySingle(
                    title=f"差分宇宙异常,UID:{dataClientMgr.currentUid}", 
                    subTitle=f"异常状态/{dataClientMgr.currentAction}", 
                    content=content, 
                    configMgr=configMgr, 
                    dataMgr=dataClientMgr, 
                    uid=dataClientMgr.currentUid
                    )
                log.info(logMgr.Info("SMTP邮件通知发送完成"))
            else:
                log.error(logMgr.Error("异常流程"))
                notifyMgr.SendNotifySingle(
                    title=f"UID:{dataClientMgr.currentUid},异常流程", 
                    subTitle=f"异常状态/异常流程", 
                    content=content, 
                    configMgr=configMgr, 
                    dataMgr=dataClientMgr, 
                    uid=dataClientMgr.currentUid
                    )
                return True
        else:
            log.info(logMgr.Info("未开启SMTP服务"))
            return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False