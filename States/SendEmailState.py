from States import *
import os,sys,time
from .BaseNotifyState import BaseNotifyState
from Hotaru.Client.NotifyHotaru import notifyMgr

class SendEmailState(BaseNotifyState):

    mStateName = 'SendEmailState'

    def OnBegin(self):
        if configMgr.mConfig[configMgr.mKey.NOTIFY_SMTP_ENABLE]:
            self.SetNotifyContent()
            
            content = ''
            content += f"<p>本次上号总计花费时长:{dataMgr.notifyContent['上号时长']}</p>"

            content += f"<p><strong>开拓力去向:</strong>"

            if dataMgr.notifyContent['副本情况']['历战余响'] > 0:
                content += f"<p>历战余响:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.currentUid]['历战余响']} - {dataMgr.notifyContent['副本情况']['历战余响']}次</p>"

            if dataMgr.notifyContent['副本情况']['拟造花萼（赤）'] > 0:
                content += f"<p>拟造花萼（赤）:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.currentUid]['拟造花萼（赤）']} - {dataMgr.notifyContent['副本情况']['拟造花萼（赤）']}次</p>"

            if dataMgr.notifyContent['副本情况']['拟造花萼（金）'] > 0:
                content += f"<p>拟造花萼（金）:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.currentUid]['拟造花萼（金）']} - {dataMgr.notifyContent['副本情况']['拟造花萼（金）']}次</p>"

            if dataMgr.notifyContent['副本情况']['凝滞虚影'] > 0:
                content += f"<p>凝滞虚影:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.currentUid]['凝滞虚影']} - {dataMgr.notifyContent['副本情况']['凝滞虚影']}次</p>"

            if dataMgr.notifyContent['副本情况']['侵蚀隧洞'] > 0:
                content += f"<p>侵蚀隧洞:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataMgr.currentUid]['侵蚀隧洞']} - {dataMgr.notifyContent['副本情况']['侵蚀隧洞']}次</p>"

            if dataMgr.notifyContent['副本情况']['模拟宇宙'] > 0:
                content += f"<p>模拟宇宙:{dataMgr.meta['模拟宇宙'][str(configMgr.mConfig[configMgr.mKey.UNIVERSE_NUMBER][dataMgr.currentUid])]} - {dataMgr.notifyContent['副本情况']['模拟宇宙']}次</p>"

            content += f"<p>下线时开拓力:<span class=important style=background-color:#40405f;color:#66ccff>{dataMgr.notifyContent['下线时开拓力']}</span></p></p>"

            content += f"<p><strong>每日完成情况</strong></p>"

            for taskName, taskValue in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid].items():

                content += f"<p><ruby>{taskName}<rt class='ttt' data-rt='{dataMgr.meta['task_score_mappings'][taskName]}'></rt></ruby>:"+(f"未完成</p>" if taskValue else "<span class=important style=background-color:#40405f;color:#66ccff>已完成</span></p>")

            content += f"<p><strong>当前活跃度</strong></p>"+(f"<blockquote>" if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid] else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataMgr.currentUid]}/500</p></blockquote>"

            content += f"<p><strong>当前模拟宇宙积分</strong></p>"+(f"<blockquote>" if configMgr.mConfig[configMgr.mKey.UNIVERSE_FIN][dataMgr.currentUid] else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][dataMgr.currentUid]}</p></blockquote>"

            content += f"<p>当前沉浸器数量:{dataMgr.currentImmersifiers}</p>"

            content += f"<p><strong>当前历战余响次数</strong></p>"+(f"<blockquote>" if configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_TIMES][dataMgr.currentUid] == 0 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_TIMES][dataMgr.currentUid]}/3</p></blockquote>"

            content += f"<p><strong>当前遗器数量</strong></p><blockquote style='background-color:rgb({(64 + (95 - 64)*(dataMgr.currentRelicCount / 2000))}, 64, {(95 - (95 - 64)*(dataMgr.currentRelicCount / 2000))});box-shadow: 3px 0 0 0 rgb({(102 + (216 - 102)*(dataMgr.currentRelicCount / 2000))}, {(204 - (204 - 89)*(dataMgr.currentRelicCount / 2000))}, {(255 - (255 - 89)*(dataMgr.currentRelicCount / 2000))}) inset;'><p>{dataMgr.currentRelicCount}/2000</p></blockquote>"

            content += f"<p><strong>最新一期忘却之庭 - 混沌回忆</strong></p><div class=post-txt-container-datetime>注意,这里不支持忘却之庭代打,仅提供信息提示</div><p>距离刷新:{dataMgr.notifyContent['混沌回忆倒计时']}</p>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataMgr.currentUid] == 12 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>层数:{configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataMgr.currentUid]}/12</p></blockquote>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataMgr.currentUid] == 36 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>星数:{configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataMgr.currentUid]}/36</p></blockquote>"

            content += f"<p><strong>最新一期虚构叙事</strong></p><div class=post-txt-container-datetime>注意,这里不支持虚构叙事代打,仅提供信息提示</div><p>距离刷新:{dataMgr.notifyContent['虚构叙事倒计时']}</p>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataMgr.currentUid] == 4 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>层数:{configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataMgr.currentUid]}/4</p></blockquote>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataMgr.currentUid] == 12 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>星数:{configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataMgr.currentUid]}/12</p></blockquote>"

            content += f"<p><strong>预计满开拓力时间</strong></p><blockquote><p>{dataMgr.notifyContent['开拓力回满时间']}</p></blockquote>"

            if len(dataMgr.notifyContent['遗器胚子']) > 0:
                content += f"<hr style=background:#d9d9d9><p><strong>遗器胚子</strong></p><div class=relicContainer>"
                for relicItem in dataMgr.notifyContent['遗器胚子']:
                    content += f"<div class=relic><p><strong>{relicItem['遗器名称']}</strong><br><span style=font-size:10px>{relicItem['遗器部位']}</span></p>"

                    content += f"<div class=relicPropContainer><p><span class=important style=color:#d97d22;background-color:#40405f;font-size:14px><strong>{relicItem['遗器主词条']}</strong></span></p>"

                    for relicSubProp in relicItem['遗器副词条']:
                        content += f"<p>{relicSubProp}</p>"

                content += "</div></div></div>"
            
            if dataMgr.currentAction == "每日任务流程":
                if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid]:
                    notifyMgr.SendNotifySingle(title=f"UID:{dataMgr.currentUid},每日已完成", subTitle=f"上号详细/{dataMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataMgr, uid=dataMgr.currentUid)
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
                else:
                    notifyMgr.SendNotifySingle(title=f"UID:{dataMgr.currentUid},每日未完成", subTitle=f"上号详细/{dataMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataMgr, uid=dataMgr.currentUid)
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
            elif dataMgr.currentAction == "模拟宇宙流程":
                notifyMgr.SendNotifySingle(title=f"UID:{dataMgr.currentUid},模拟宇宙已结束", subTitle=f"上号详细/{dataMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataMgr, uid=dataMgr.currentUid)
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