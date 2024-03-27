from States import *
from Hotaru.Client.DataClientHotaru import dataMgr
from .BaseNotifyState import BaseNotifyState
from Hotaru.Client.NotifyHotaru import notifyMgr

class SendEmailExceptionState(BaseNotifyState):

    mStateName = 'SendEmailExceptionState'

    def OnBegin(self):
        if configMgr.mConfig[configMgr.mKey.NOTIFY_SMTP_ENABLE]:
            self.SetNotifyContent()
            
            content = dataMgr.tempText
            
            if dataMgr.currentAction == "每日任务流程":
                if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid]:
                    notifyMgr.SendNotifySingle(title=f"UID:{dataMgr.currentUid},每日异常", subTitle=f"异常状态/{dataMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataMgr, uid=dataMgr.currentUid)
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
                else:
                    notifyMgr.SendNotifySingle(title=f"UID:{dataMgr.currentUid},每日异常", subTitle=f"异常状态/{dataMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataMgr, uid=dataMgr.currentUid)
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
            elif dataMgr.currentAction == "模拟宇宙流程":
                notifyMgr.SendNotifySingle(title=f"UID:{dataMgr.currentUid},模拟宇宙异常", subTitle=f"异常状态/{dataMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataMgr, uid=dataMgr.currentUid)
                log.info(logMgr.Info("SMTP邮件通知发送完成"))
            else:
                log.error(logMgr.Error("异常的Action"))
                return True
        else:
            log.info(logMgr.Info("未开启SMTP服务"))

        return False

    def OnRunning(self):
        return False

    def OnExit(self):
        return False