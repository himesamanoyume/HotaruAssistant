from States.Client import *
from .BaseNotifyState import BaseNotifyState
from Hotaru.Client.NotifyHotaru import notifyMgr
import os

class SendEmailState(BaseNotifyState):

    mStateName = 'SendEmailState'

    def OnBegin(self):
        if configMgr.mConfig[configMgr.mKey.NOTIFY_SMTP_ENABLE]:
            self.SetNotifyContent()
            
            content = ''
            content += f"<p>本次上号总计花费时长:{dataClientMgr.notifyContent['上号时长']}</p>"

            if dataClientMgr.passRemaining != '':
                content += f"<p>月卡剩余:<span class=important style=background-color:#40405f;color:#66ccff>{dataClientMgr.passRemaining}</span></p>"

            content += f"<p><strong>开拓力去向:</strong>"

            if dataClientMgr.notifyContent['副本情况']['历战余响'] > 0:
                content += f"<p>历战余响:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataClientMgr.currentUid]['历战余响']} - {dataClientMgr.notifyContent['副本情况']['历战余响']}次</p>"

            if dataClientMgr.notifyContent['副本情况']['拟造花萼（赤）'] > 0:
                content += f"<p>拟造花萼（赤）:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataClientMgr.currentUid]['拟造花萼（赤）']} - {dataClientMgr.notifyContent['副本情况']['拟造花萼（赤）']}次</p>"

            if dataClientMgr.notifyContent['副本情况']['拟造花萼（金）'] > 0:
                content += f"<p>拟造花萼（金）:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataClientMgr.currentUid]['拟造花萼（金）']} - {dataClientMgr.notifyContent['副本情况']['拟造花萼（金）']}次</p>"

            if dataClientMgr.notifyContent['副本情况']['凝滞虚影'] > 0:
                content += f"<p>凝滞虚影:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataClientMgr.currentUid]['凝滞虚影']} - {dataClientMgr.notifyContent['副本情况']['凝滞虚影']}次</p>"

            if dataClientMgr.notifyContent['副本情况']['侵蚀隧洞'] > 0:
                content += f"<p>侵蚀隧洞:{configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][dataClientMgr.currentUid]['侵蚀隧洞']} - {dataClientMgr.notifyContent['副本情况']['侵蚀隧洞']}次</p>"

            if dataClientMgr.notifyContent['副本情况']['模拟宇宙'] > 0:
                content += f"<p>模拟宇宙:{dataClientMgr.meta['模拟宇宙'][str(configMgr.mConfig[configMgr.mKey.UNIVERSE_NUMBER][dataClientMgr.currentUid])]} - {dataClientMgr.notifyContent['副本情况']['模拟宇宙']}次</p>"

            content += f"<p>下线时开拓力:<span class=important style=background-color:#40405f;color:#66ccff>{dataClientMgr.currentPower}</span></p></p>"

            if os.path.exists(f'./screenshots/{dataClientMgr.currentUid}/daily.png'):
                img = f"<img loading='lazy' src='cid:dailyImg'>"
            else:
                img = f"<p>未检测到每日任务截图</p>"

            content += f"<p><strong>每日完成情况</strong></p>{img}<div class=post-txt-container-datetime>注意,如果截图中每日未完成但脚本显示已完成,建议立刻到后台修改每日完成情况,以免导致运行当天的每日任务流程时脚本不会去完成剩下的每日任务</div>"

            for taskName, taskValue in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid].items():

                content += f"<p><ruby>{taskName}<rt class='ttt' data-rt='{dataClientMgr.meta['task_score_mappings'][taskName]}'></rt></ruby>:"+(f"未完成</p>" if taskValue else "<span class=important style=background-color:#40405f;color:#66ccff>已完成</span></p>")

            content += f"<p><strong>当前活跃度</strong></p>"+(f"<blockquote>" if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataClientMgr.currentUid] else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][dataClientMgr.currentUid]}/500</p></blockquote>"

            content += f"<p><strong>当前模拟宇宙积分</strong></p>"+(f"<blockquote>" if configMgr.mConfig[configMgr.mKey.UNIVERSE_FIN][dataClientMgr.currentUid] else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][dataClientMgr.currentUid]}</p></blockquote>"

            content += f"<p>当前沉浸器数量:{dataClientMgr.currentImmersifiers}</p>"

            content += f"<p><strong>当前历战余响次数</strong></p>"+(f"<blockquote>" if configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_TIMES][dataClientMgr.currentUid] == 0 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_TIMES][dataClientMgr.currentUid]}/3</p></blockquote>"

            content += f"<p><strong>当前遗器数量</strong></p><blockquote style='background-color:rgb({(64 + (95 - 64)*(dataClientMgr.currentRelicCount / 2000))}, 64, {(95 - (95 - 64)*(dataClientMgr.currentRelicCount / 2000))});box-shadow: 3px 0 0 0 rgb({(102 + (216 - 102)*(dataClientMgr.currentRelicCount / 2000))}, {(204 - (204 - 89)*(dataClientMgr.currentRelicCount / 2000))}, {(255 - (255 - 89)*(dataClientMgr.currentRelicCount / 2000))}) inset;'><p>{dataClientMgr.currentRelicCount}/2000</p></blockquote>"

            content += f"<p><strong>最新一期忘却之庭 - 混沌回忆</strong></p><div class=post-txt-container-datetime>注意,脚本不支持忘却之庭代打,仅提供信息提示</div><p>距离刷新:{dataClientMgr.notifyContent['混沌回忆1倒计时']}</p>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataClientMgr.currentUid][0] == 12 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>层数:{configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataClientMgr.currentUid][0]}/12</p></blockquote>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataClientMgr.currentUid][0] == 36 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>星数:{configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataClientMgr.currentUid][0]}/36</p></blockquote>"

            if not dataClientMgr.notifyContent['混沌回忆2层数'] == -1:
                content += f"<p><strong>上期忘却之庭 - 混沌回忆</strong></p><p>距离刷新:{dataClientMgr.notifyContent['混沌回忆2倒计时']}</p>"

                content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataClientMgr.currentUid][1] == 12 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>层数:{configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_LEVELS][dataClientMgr.currentUid][1]}/12</p></blockquote>"

                content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataClientMgr.currentUid][1] == 36 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>星数:{configMgr.mConfig[configMgr.mKey.FORGOTTENHALL_STARS][dataClientMgr.currentUid][1]}/36</p></blockquote>"

            content += f"<p><strong>最新一期虚构叙事</strong></p><div class=post-txt-container-datetime>注意,脚本不支持虚构叙事代打,仅提供信息提示</div><p>距离刷新:{dataClientMgr.notifyContent['虚构叙事1倒计时']}</p>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataClientMgr.currentUid][0] == 4 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>层数:{configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataClientMgr.currentUid][0]}/4</p></blockquote>"

            content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataClientMgr.currentUid][0] == 12 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>星数:{configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataClientMgr.currentUid][0]}/12</p></blockquote>"

            if not dataClientMgr.notifyContent['虚构叙事2层数'] == -1:
                content += f"<p><strong>上期虚构叙事</strong></p><p>距离刷新:{dataClientMgr.notifyContent['虚构叙事2倒计时']}</p>"

                content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataClientMgr.currentUid][1] == 4 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>层数:{configMgr.mConfig[configMgr.mKey.PUREFICTION_LEVELS][dataClientMgr.currentUid][1]}/4</p></blockquote>"

                content += (f"<blockquote>" if configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataClientMgr.currentUid][1] == 12 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>星数:{configMgr.mConfig[configMgr.mKey.PUREFICTION_STARS][dataClientMgr.currentUid][1]}/12</p></blockquote>"

            content += f"<p><strong>预计满开拓力时间</strong></p><blockquote><p>{dataClientMgr.notifyContent['开拓力回满时间']}</p></blockquote>"

            tempContent = ''

            if len(dataClientMgr.notifyContent['遗器胚子']) > 0:
                for relicItem in dataClientMgr.notifyContent['遗器胚子']:
                    
                    tempList = ''
                    for relicSubProp in relicItem['遗器副词条']:
                        tempList += f"<p>{relicSubProp}</p>"

                    tempContent += f"""
                    <div class='relic'>
                        <p>
                            <strong>{relicItem['遗器名称']}</strong>
                            <br>
                            <span style=font-size:10px>{relicItem['遗器部位']}</span>
                        </p>
                        <div class='relicPropContainer'>
                            <p>
                                <span class=important style=color:#d97d22;background-color:#40405f;font-size:14px>
                                <strong>{relicItem['遗器主词条']}</strong>
                                </span>
                            </p>
                            {tempList}
                        </div>
                    </div>
                    """

                content += f"""
                <hr style=background:#d9d9d9>
                <p>
                    <strong>遗器胚子</strong>
                </p>
                <div class='relicContainer'>
                    {tempContent}
                </div>
                """
            
            if dataClientMgr.currentAction == "每日任务流程":
                if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataClientMgr.currentUid]:
                    notifyMgr.SendNotifySingle(title=f"UID:{dataClientMgr.currentUid},每日已完成", subTitle=f"上号详细/{dataClientMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataClientMgr, uid=dataClientMgr.currentUid)
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
                else:
                    notifyMgr.SendNotifySingle(title=f"UID:{dataClientMgr.currentUid},每日未完成", subTitle=f"上号详细/{dataClientMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataClientMgr, uid=dataClientMgr.currentUid)
                    log.info(logMgr.Info("SMTP邮件通知发送完成"))
            elif dataClientMgr.currentAction == "模拟宇宙流程":
                notifyMgr.SendNotifySingle(title=f"UID:{dataClientMgr.currentUid},模拟宇宙已结束", subTitle=f"上号详细/{dataClientMgr.currentAction}", content=content, configMgr=configMgr, dataMgr=dataClientMgr, uid=dataClientMgr.currentUid)
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