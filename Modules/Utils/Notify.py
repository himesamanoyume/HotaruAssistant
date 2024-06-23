import json,requests,time,smtplib,base64,os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from Modules.Utils.ConfigKey import ConfigKey

class Notify:

    @staticmethod
    def GetGithubAnnList(dataMgr):
        if dataMgr.YW5ub3VuY2VtZW50:
            annList = dataMgr.YW5ub3VuY2VtZW50
        else:
            annList = [{"Title":"{Y2NvbnRlbnR0}".format(Y2NvbnRlbnR0=base64.b64decode("5pyq6IO96I635Y+W5Yiw5YWs5ZGK").decode('utf-8')),"Content":"{Y2NvbnRlbnR0}".format(Y2NvbnRlbnR0=base64.b64decode("5pyq6IO96I635Y+W5Yiw5YWs5ZGK").decode('utf-8'))}]

        return annList
    
    @staticmethod
    def CreateHotaruUpdateContent(dataMgr):
        isLatestTxt = dataMgr.isLatestTxt
        updateList = [{"Content":isLatestTxt}]
        return updateList
    
    @staticmethod
    def CreateGithubAnnListContent(dataMgr):
        annList = Notify.GetGithubAnnList(dataMgr)
        content = ''
        for item in annList:
            content += f"<div style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;margin:10px 0 0 0;'><p style='margin: 0 20px 0 20px;'><b>{item['Title']}</b></p><p style='font-size: 12px;line-height: 20px;display: inline-block;transition-duration: .2s;'>{item['Content']}</p></div>"

        return content
    
    @staticmethod
    def CalcProgress(startTime, endTime):
        startTimestamp = time.mktime(time.strptime(startTime, "%Y-%m-%d %H:%M:%S"))
        endTimestamp = time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S"))
        progress = (time.time() - startTimestamp) / (endTimestamp - startTimestamp)
        totalTime = endTimestamp - time.time()
        day = int(totalTime // 86400)
        hour = int((totalTime - day * 86400) // 3600)
        return progress, day, hour

    @staticmethod
    def GetOfficialAnnList(isInfomation = True):
        r = requests.get("https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&channel_id=1&level=1&platform=pc&region=prod_gf_cn&uid=1")
        if r.status_code == 200:
            data = json.loads(r.text)
            if isInfomation:
                data = data['data']['pic_list'][0]['type_list'][0]['list']
            else:
                data = data['data']['list'][0]['list']

            dataList = list()
            for item in data:
                title = item['title']
                if title == '':
                    continue

                startTime = item['start_time']
                endTime = item['end_time']
                progress, day, hour = Notify.CalcProgress(startTime, endTime)
                dataList.append({"title":title,"start_time":startTime,"end_time":endTime,"progress": progress, "day":day, "hour":hour})

            return dataList
        else:
            if isInfomation:
                dataList = [{"title":"未能获取到官方资讯,请刷新页面重试","day":"0","hour":"0", "start_time":"0","end_time":"0", "progress":1}]
            else:
                dataList = [{"title":"未能获取到官方公告,请刷新页面重试","day":"0","hour":"0", "start_time":"0","end_time":"0", "progress":1}]
            return dataList
                
    @staticmethod
    def CreateOfficialContent(isInfomation = True):
        datalist = Notify.GetOfficialAnnList(isInfomation)
        if isInfomation:
            content = "<p>简易官方资讯,进度条仅代表邮件发送时距离结束的进度!</p><div style='display: inline-flex;justify-content: space-between;flex-wrap: wrap;-ms-flex-wrap: wrap;-webkit-flex-wrap: wrap;flex: none;'>"
        else:
            content = "<p>简易官方公告,进度条仅代表邮件发送时距离结束的进度!</p><div style='display: inline-flex;justify-content: space-between;flex-wrap: wrap;-ms-flex-wrap: wrap;-webkit-flex-wrap: wrap;flex: none;'>"
        
        for item in datalist:
            content += f"<div style='background-color:#40405f;margin:10px 0 0 0;width:49.3%;position:relative;'><p style='margin: 0 20px 0 20px;'><b>{item['title']}</b></p><p style='font-size: 12px;line-height: 20px;display: inline-block;transition-duration: .2s;'>{item['day']} 天 {item['hour']} 时后结束<br>{item['start_time']} - {item['end_time']}</p><div style='background-color: #66ccff;width:{item['progress'] * 100}%;max-width:100%;height:3px;bottom:0;position:absolute;'></div></div>"

        content += '</div>'

        return content
    
    @staticmethod
    def CreateConfigContent(detailContent, uid, dataMgr, configMgr):
        detailContent += f"<hr style=background:#d9d9d9><p><strong>配置详细</strong></p><div class=post-txt-container-datetime>该配置显示了当要挑战副本时会选择什么副本,如果配置与需求不符或需求有变化需要到后台进行调整</div>"
        detailContent += f"<p>今天每日清开拓力时将要打的副本类型:<span class=important style=background-color:#40405f;color:#66ccff>{configMgr.mConfig[ConfigKey.INSTANCE_TYPE][uid][0]}</span></p>"
        detailContent += f"<p>不同副本类型下的副本名称:</p>"

        goldenText = ''
        goldenText = dataMgr.meta['拟造花萼（金）'][configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['拟造花萼（金）']]

        crimsonText = ''
        crimsonText = dataMgr.meta['拟造花萼（赤）'][configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['拟造花萼（赤）']][0]

        shadowText = ''
        shadowText = dataMgr.meta['凝滞虚影'][configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['凝滞虚影']][0]

        cavernText = ''
        cavernText = dataMgr.meta['侵蚀隧洞'][configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['侵蚀隧洞']][0]

        echoofwarText = ''
        echoofwarText = dataMgr.meta['历战余响'][configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['历战余响']]

        detailContent += f"<p>拟造花萼（金）:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{goldenText}<rt class='ttt' style='background-color: unset;' data-rt='{configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['拟造花萼（金）']}'></rt></ruby></span></p>"

        detailContent += f"<p>拟造花萼（赤）:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{crimsonText}<rt class='ttt' style='background-color: unset;' data-rt='{configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['拟造花萼（赤）']}'></rt></ruby></span></p>"

        detailContent += f"<p>凝滞虚影:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{shadowText}<rt class='ttt' style='background-color: unset;' data-rt='{configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['凝滞虚影']}'></rt></ruby></span></p>"

        detailContent += f"<p>侵蚀隧洞:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{cavernText}<rt class='ttt' style='background-color: unset;' data-rt='{configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['侵蚀隧洞']}'></rt></ruby></span></p>"

        detailContent += f"<p>是否清空3次历战余响:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if configMgr.mConfig[ConfigKey.ECHO_OF_WAR_ENABLE][uid] else '否'}</span></p>"

        detailContent += f"<p>历战余响:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{echoofwarText}<rt class='ttt' style='background-color: unset;' data-rt='{configMgr.mConfig[ConfigKey.INSTANCE_NAMES][uid]['历战余响']}'></rt></ruby></span></p>"

        detailContent += f"<p>是否分解遗器:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if configMgr.mConfig[ConfigKey.RELICS_SALVAGE_ENABLE][uid] else '否'}</span></p>"

        detailContent += f"<p>若开启分解,是否分解4星遗器:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if configMgr.mConfig[ConfigKey.RELICS_SALVAGE_4STAR_ENABLE][uid] else '否'}</span></p>"

        detailContent += f"<p>若开启分解,是否分解5星遗器:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if configMgr.mConfig[ConfigKey.RELICS_SALVAGE_5STAR_ENABLE][uid] else '否'}</span></p>"

        detailContent += f"<p>若分解5星遗器,是否分解为遗器经验材料:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if configMgr.mConfig[ConfigKey.RELICS_SALVAGE_5STAR_TO_EXP][uid] else '否'}</span></p>"

        detailContent += f"<p>当遗器数量达到何值时触发遗器分解:<span class=important style=background-color:#40405f;color:#66ccff>{configMgr.mConfig[ConfigKey.RELICS_THRESHOLD_COUNT][uid]}</span></p>"

        if configMgr.mConfig[ConfigKey.UNIVERSE_NUMBER][uid] in [3,4,5,6,7,8]:
            worldNumber = dataMgr.meta['模拟宇宙'][str(configMgr.mConfig[ConfigKey.UNIVERSE_NUMBER][uid])]['名称']
            worldRelics = dataMgr.meta['模拟宇宙'][str(configMgr.mConfig[ConfigKey.UNIVERSE_NUMBER][uid])]['遗器']
        else:
            worldNumber = '世界选择有误'
            worldRelics = ''

        universeContent = ''
        universeContent += f"<p>模拟宇宙:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{worldRelics}<rt class='ttt' style='background-color: unset;' data-rt='{worldNumber}'></rt></ruby></span></p>"

        return detailContent, universeContent

    @staticmethod
    def CreateAsideContent(dataMgr):
        asideContent = f"""
        <aside class=info-container>
                            <div class=info-container-inner id=info-container-inner style='margin-top:10px'>
                                <div class=info style=background-color:#2b2b2b>
                                    <div class=fiximg style=width:100%;border-bottom-left-radius:0;border-bottom-right-radius:0;display:block>
                                        <div class=fiximg__container style=display:block;margin:0>
                                            <img class=info-icon loading=lazy src=https://blog.himesamanoyume.top/usericon.webp style=margin-top:20px;max-height:185px;border-radius:3px;max-width:185px;width:100%;border:0;background-color:#66ccff>
                                        </div>
                                    </div>
                                    <div class=info-name style=color:#d9d9d9>
                                        <ruby>姫様の夢<rt class='ttt' data-rt='Himesamanoyume'></rt></ruby>
                                    </div>
                                    <div class=info-txt style=color:#d9d9d9>
                                        夏河小俘虏
                                    </div>
                                </div>
                            </div>
                        </aside>
                    </div>
                </main>
                <footer class=footer style=color:#d9d9d9>
                    <div class=footer-content>
                        Copyright © 2021-2024 @姫様の夢
                    </div>
                    <div class=footer-content>
                        本软件永久免费,若被收取了费用说明您被骗了!
                    </div>
                    <div class=footer-content>
                        <a href='https://github.com/himesamanoyume/HotaruAssistant' target='_blank' >HotaruAssistant</a> {dataMgr.version}
                    </div>
                </footer>
            </div>
        """
        return asideContent

    @staticmethod
    def CreateHeadContent(title, dataMgr, configMgr, isNotifyWeb=False):
        if not isNotifyWeb:
            if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid]:
                img = f"<img loading='lazy' src='cid:bgHotaru'>"
            else:
                img = f"<img loading='lazy' src='cid:bgNoHotaru'>"
        else:
            img = ""
        headContent = f"""
        <div class=body style=background-color:#3a3a3a>
            <style>{dataMgr.htmlStyle}</style>
                <header class=header style=position:sticky>
                    <nav class=nav style='margin:0 15px;justify-content:center;background-color:#2b2b2b'>
                        <span class=blogName style=color:#d9d9d9;text-align:center;font-size:x-large; id=nav-index>
                            流萤的秘密基地
                        </span>
                    </nav>
                </header>
                <main class=main>
                    <div class=home-container>
                        <div class=post-container style=margin:0;box-sizing:border-box;max-width:100%;width:100%;height:100%;border:0>
                            <div class=post-sub-container>
                                <div class="post-container-sticky">
                                    <div class=post style=background-color:#2b2b2b>
                                        <div class=post-Img-container style=max-height:none>
                                            {img}
                                        </div>
                                        <div class=post-txt-container>
                                            <div class=post-txt-container-title style=color:#d9d9d9>
                                                <h4 style=color:#66ccff>
                                                    {title}
                                                </h4>
                                            </div>
                        """
        return headContent
    
    @staticmethod
    def LoginSMTP(configMgr):
        sendHostEmail = smtplib.SMTP(configMgr.mConfig[ConfigKey.NOTIFY_SMTP_HOST], configMgr.mConfig[ConfigKey.NOTIFY_SMTP_PORT])
        sendHostEmail.login(configMgr.mConfig[ConfigKey.NOTIFY_SMTP_USER], configMgr.mConfig[ConfigKey.NOTIFY_SMTP_PASSWORD])
        return sendHostEmail

    @staticmethod
    def SendNotifyAll(title, subTitle, content, configMgr, dataMgr, isNotifyWeb=False):
        sendHostEmail = Notify.LoginSMTP(configMgr)
        
        detailContent = content

        for index, value in configMgr.mConfig[ConfigKey.NOTIFY_SMTP_TO].items():
            emailObject = MIMEMultipart()
            themeObject = Header(title, 'utf-8').encode()

            emailObject['subject'] = themeObject
            emailObject['From'] = configMgr.mConfig[ConfigKey.NOTIFY_SMTP_FROM]

            htmlStr=f"""
                {Notify.CreateHeadContent(subTitle, dataMgr, isNotifyWeb=isNotifyWeb)}
                                            <section class=post-detail-txt style=color:#d9d9d9>
                                                {Notify.CreateGithubAnnListContent(dataMgr)}
                                                {detailContent}
                                                <hr style=background:#d9d9d9>
                                                {Notify.CreateOfficialContent(False)}
                                            </section>
                                            <p>
                                                <div class=post-txt-container-datetime style=color:#d9d9d9>
                                                    请不要绑定qq邮箱以外的邮箱,会使邮件的页面非常错乱!
                                                </div>
                                            </p>
                                            <div class=post-txt-container-datetime style=color:#d9d9d9>
                                            {str(datetime.now()).split('.')[0]}
                                            <span class=important style=background-color:#40405f;color:#66ccff>
                                                [{index}]
                                            </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {Notify.CreateAsideContent(dataMgr)}
            """
            html = f"{htmlStr}"
            emailObject.attach(MIMEText(html,'html','utf-8'))
            emailObject['To'] = value
            sendHostEmail.sendmail(configMgr.mConfig[ConfigKey.NOTIFY_SMTP_FROM], configMgr.mConfig[ConfigKey.NOTIFY_SMTP_TO][index], str(emailObject))
        
        sendHostEmail.sendmail(configMgr.mConfig[ConfigKey.NOTIFY_SMTP_FROM], configMgr.mConfig[ConfigKey.NOTIFY_SMTP_MASTER], str(emailObject))
        sendHostEmail.quit()

    @staticmethod
    def SendNotifySingle(title, subTitle, content, configMgr, dataMgr, uid, previewContent = None, isNotifyWeb = False):
        sendHostEmail = Notify.LoginSMTP(configMgr)
        
        detailContent = content

        emailObject = MIMEMultipart()
        themeObject = Header(title, 'utf-8').encode()

        emailObject['subject'] = themeObject
        emailObject['From'] = configMgr.mConfig[ConfigKey.NOTIFY_SMTP_FROM]

        detailContent, universeContent = Notify.CreateConfigContent(detailContent, uid, dataMgr, configMgr)

        htmlStr=f"""
            <span style="display: none;">{previewContent}</span>
            {Notify.CreateHeadContent(subTitle, dataMgr, configMgr, isNotifyWeb=isNotifyWeb)}
                                            <section class=post-detail-txt style=color:#d9d9d9>
                                                {Notify.CreateGithubAnnListContent(dataMgr)}
                                                <p>{detailContent}{universeContent}</p>
                                                <hr style=background:#d9d9d9>
                                                {Notify.CreateOfficialContent(False)}
                                            </section>
                                            <p>
                                                <div class=post-txt-container-datetime style=color:#d9d9d9>
                                                    请不要绑定qq邮箱以外的邮箱,会使邮件的页面非常错乱!
                                                </div>
                                            </p>
                                            <div class=post-txt-container-datetime style=color:#d9d9d9>
                                            {str(datetime.now()).split('.')[0]}
                                            <span class=important style=background-color:#40405f;color:#66ccff>
                                                [{uid}]
                                            </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {Notify.CreateAsideContent(dataMgr)}
            """

        html = f"{htmlStr}"
        emailObject.attach(MIMEText(html,'html','utf-8'))
        if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][uid]:
            with open('./assets/static/images/web/bg_Hotaru.png', 'rb') as hotaruPng:
                bgHotaru = MIMEImage(hotaruPng.read())
                bgHotaru.add_header('Content-ID', '<bgHotaru>')
                emailObject.attach(bgHotaru)
                hotaruPng.close()
        else:
            with open('./assets/static/images/web/bg_noHotaru.png', 'rb') as noHotaruPng:
                bgNoHotaru = MIMEImage(noHotaruPng.read())
                bgNoHotaru.add_header('Content-ID', '<bgNoHotaru>')
                emailObject.attach(bgNoHotaru)
                noHotaruPng.close()

        if os.path.exists(f'./screenshots/{uid}/daily.png'):
            with open(f'./screenshots/{uid}/daily.png', 'rb') as dailyScreenshotPng:
                dailyScreenshot = MIMEImage(dailyScreenshotPng.read())
                dailyScreenshot.add_header('Content-ID', '<dailyImg>')
                emailObject.attach(dailyScreenshot)
                dailyScreenshotPng.close()

        emailObject['To'] = configMgr.mConfig[ConfigKey.NOTIFY_SMTP_MASTER]

        sendHostEmail.sendmail(configMgr.mConfig[ConfigKey.NOTIFY_SMTP_FROM], configMgr.mConfig[ConfigKey.NOTIFY_SMTP_TO][uid], str(emailObject))
        sendHostEmail.sendmail(configMgr.mConfig[ConfigKey.NOTIFY_SMTP_FROM], configMgr.mConfig[ConfigKey.NOTIFY_SMTP_USER], str(emailObject))

        sendHostEmail.quit()
        return True

    

        