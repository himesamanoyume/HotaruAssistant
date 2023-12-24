import base64
# coding=utf-8
import requests
from onepush import get_notifier
from managers.logger_manager import logger
from managers.config_manager import config
from tasks.daily.utils import Utils
from managers.translate_manager import _
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import random
from datetime import datetime
from email.mime.base import MIMEBase
import time
from email import encoders
import os
from managers.utils_manager import gu
from tasks.daily.webtools import WebTools


class Notify:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.notifiers = {
                "winotify": False,
                "bark": False,
                "custom": False,
                "gocqhttp": False,
                "dingtalk": False,
                "discord": False,
                "pushplus": False,
                "pushdeer": False,
                "qmsg": False,
                "serverchan": False,
                "serverchanturbo": False,
                "smtp": False,
                "telegram": False,
                "wechatworkapp": False,
                "wechatworkbot": False,
                "lark": False
            }
        return cls._instance

    def set_notifier(self, notifier_name, enable, params=None):
        self.notifiers[notifier_name] = enable

        if params:
            setattr(self, notifier_name, params)

    def _send_notification(self, notifier_name, title, content, isSingle):
        if self.notifiers.get(notifier_name, False):

            # if notifier_name == "winotify":
            #     self._send_notification_by_winotify(title, content)
            #     return

            # if notifier_name == "pushplus":
            #     content = '.' if content is None or content == '' else content
            
            if notifier_name == "smtp":
                self._send_notification_by_smtp(title, content, isSingle)
                return

            notifier_params = getattr(self, notifier_name, None)
            if notifier_params:
                n = get_notifier(notifier_name)
                try:
                    response = n.notify(**notifier_params,
                                        title=title, content=content)
                    logger.info(gu(f"{notifier_name.capitalize()} 通知发送完成"))
                except Exception as e:
                    logger.error(gu(f"{notifier_name.capitalize()} 通知发送失败"))
                    logger.error(f"{e}")

    def _send_notification_with_image(self, notifier_name, title, content, image_io):
        if not self.notifiers.get(notifier_name, False):
            return

        if notifier_name == "telegram":
            notifier_params = getattr(self, notifier_name, None)
            if notifier_params:
                token = notifier_params["token"]
                chat_id = notifier_params["userid"]
                api_url = notifier_params["api_url"] if "api_url" in notifier_params else "api.telegram.org"
                tgurl = f"https://{api_url}/bot{token}/sendPhoto"
                message = content
                if title and content:
                    message = '{}\n\n{}'.format(title, content)
                if title and not content:
                    message = title
                files = {
                    'photo': ('merged_image.jpg', image_io.getvalue(), 'image/jpeg'),
                    'chat_id': (None, chat_id),
                    'caption': (None, message)
                    # 'text': (None, " ")
                }
                try:
                    response = requests.post(tgurl, files=files)
                    logger.info(_("{notifier_name} 通知发送完成").format(notifier_name=notifier_name.capitalize()))
                except Exception as e:
                    logger.error(_("{notifier_name} 通知发送失败").format(notifier_name=notifier_name.capitalize()))
                    logger.error(f"{e}")

        elif notifier_name == "gocqhttp":
            notifier_params = getattr(self, notifier_name, None)
            if notifier_params:
                n = get_notifier(notifier_name)
                base64_str = base64.b64encode(image_io.getvalue()).decode()
                cq_code = f"[CQ:image,file=base64://{base64_str}]"
                content = content + cq_code if content else cq_code
                try:
                    response = n.notify(**notifier_params, title=title, content=content)
                    logger.info(_("{notifier_name} 通知发送完成").format(notifier_name=notifier_name.capitalize()))
                except Exception as e:
                    logger.error(_("{notifier_name} 通知发送失败").format(notifier_name=notifier_name.capitalize()))
                    logger.error(f"{e}")

    def get_single_mp4_file(directory):
        mp4_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
        if len(mp4_files) == 1:
            return mp4_files[0]
        else:
            return None

    def _send_notification_by_smtp(self, title, contentTitle, isSingle=False):
        config.reload()
        sendHostEmail = smtplib.SMTP(config.notify_smtp_host, config.notify_smtp_port)
        sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
        emailObject = MIMEMultipart()
        themeObject = Header(title, 'utf-8').encode()

        new_power = Utils._content['new_power']
        uid = Utils._content['uid']

        emailObject['subject'] = themeObject
        emailObject['From'] = config.notify_smtp_From
        emailObject['To'] = config.notify_smtp_To[uid]

        date = Utils._content['date']
        date = str(date).split('.')[0]
        full_power_time = Utils._content['full_power_time']
        full_power_time = str(full_power_time).split('.')[0]
        running_time = f"<p>本次上号总计花费时长:{Utils._content['running_time']}</p>"
        multi_content = Utils._content['multi_content']
        relic_content = Utils._content['relic_content']
        if relic_content == '':
            relic_content = '<p>无</p>'
        multi_content += f"<p><strong>每日完成情况</strong></p>"

        for i in range(6):
            multi_content += f"<p><ruby>{Utils._content[f'daily_0{i}']}<rt class='ttt' data-rt='{Utils._content[f'daily_0{i}_score']}'></rt></ruby>:"+(f"未完成</p>" if Utils._content[f'daily_0{i}_value'] else "<span class=important style=background-color:#40405f;color:#66ccff>已完成</span></p>")

        account_active_content = ("<blockquote><p>" if not config.account_active[uid]['ActiveDay'] <= 3 else "<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'><p>")+f"激活天数剩余:{round((config.account_active[uid]['ActiveDay'] - config.account_active[uid]['CostDay']),3)}天</p><p>过期时间:{str(datetime.fromtimestamp(config.account_active[uid]['ExpirationDate'])).split('.')[0]}</p></blockquote>"

        multi_content += f"<p><strong>当前活跃度</strong></p>"+(f"<blockquote>" if config.daily_tasks_fin[uid] else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{Utils._content['daily_tasks_score']}/500</p></blockquote>"

        multi_content += f"<p><strong>当前模拟宇宙积分</strong></p>"+(f"<blockquote>" if config.universe_fin[uid] else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{Utils._content['current_universe_score']}/{Utils._content['max_universe_score']}</p></blockquote>"

        multi_content += f"<p>当前沉浸器数量:{Utils._immersifiers}</p>"

        multi_content += f"<p><strong>当前历战余响次数</strong></p>"+(f"<blockquote>" if config.echo_of_war_times[uid] == 0 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>{config.echo_of_war_times[uid]}/3</p></blockquote>"

        multi_content += f"<p><strong>当前遗器数量</strong></p><blockquote style='background-color:rgb({(64 + (95 - 64)*(Utils._relicCount / 1500))}, 64, {(95 - (95 - 64)*(Utils._relicCount / 1500))});box-shadow: 3px 0 0 0 rgb({(102 + (216 - 102)*(Utils._relicCount / 1500))}, {(204 - (204 - 89)*(Utils._relicCount / 1500))}, {(255 - (255 - 89)*(Utils._relicCount / 1500))}) inset;'><p>{Utils._relicCount}/1500</p></blockquote>"

        multi_content += f"<p><strong>当前忘却之庭 - 混沌回忆</strong></p><div class=post-txt-container-datetime>注意,这里不支持忘却之庭代打,仅提供信息提示</div><p>距离刷新:{Utils._content['countdownText']}</p>"

        multi_content += (f"<blockquote>" if config.forgottenhall_levels[uid] == 10 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>层数:{config.forgottenhall_levels[uid]}/10</p></blockquote>"

        multi_content += (f"<blockquote>" if config.forgottenhall_stars[uid] == 30 else f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'>")+f"<p>星数:{config.forgottenhall_stars[uid]}/30</p></blockquote>"

        multi_content += f"<p><strong>预计满开拓力时间</strong></p><blockquote><p>{full_power_time}</p></blockquote>"

        multi_content, universe_content = WebTools.config_content(multi_content, uid)
        
        htmlStr=f"""
            {WebTools.head_content(contentTitle)}
                                <section class=post-detail-txt style=color:#d9d9d9>
                                    {account_active_content}
                                    {WebTools.official_content()}
                                    {running_time}
                                    <p>
                                        <strong>开拓力去向:</strong>
                                        <p>
                                            下线时开拓力:
                                            <span class=important style=background-color:#40405f;color:#66ccff>
                                                {new_power}
                                            </span>
                                        </p>
                                    </p>
                                    <p>{multi_content}{universe_content}</p>
                                    <hr style=background:#d9d9d9>
                                    <p><strong>遗器胚子</strong></p>
                                    <div class=relicContainer>
                                        {relic_content}
                                    </div>
                                </section>
                                <p>
                                    <div class=post-txt-container-datetime style=color:#d9d9d9>
                                        请尽量不要绑定qq邮箱以外的邮箱,会使邮件的页面非常错乱!
                                    </div>
                                </p>
                                <div class=post-txt-container-datetime style=color:#d9d9d9>
                                    {date}
                                    <span class=important style=background-color:#40405f;color:#66ccff>
                                        [{uid}]
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    {WebTools.aside_content()}
        """

        html=f"{htmlStr}"
        emailObject.attach(MIMEText(html,'html','utf-8'))
        time.sleep(5)

        # 使用方法
        if config.recording_enable:
            directory = './records'  # 你的文件夹路径
            mp4_file = Notify.get_single_mp4_file(directory)
            if mp4_file is not None:
                mp4_file_path = f"{directory}/{mp4_file}"
                size = os.path.getsize(mp4_file_path)
                logger.info(gu(f"视频大小为:{size}/50000000"))
                if size < 50000000:
                    try:
                        att = open(mp4_file_path, 'rb')
                        part = MIMEBase('application','octet-stream')
                        part.set_payload((att).read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', "attachment; filename= %s" % mp4_file)
                        emailObject.attach(part)
                    except Exception as e:
                        nowtime = time.time()
                        logger.error(gu(f"{nowtime},邮件错误:{e}"))
                        raise Exception(f"{nowtime},邮件错误:{e}")
                else:
                    logger.warning(gu("由于视频文件过大,取消附件"))

        
        import threading
        if isSingle:
            t = threading.Thread(target=Notify.send_mail(config.notify_smtp_From, config.notify_smtp_master, sendHostEmail, str(emailObject)))
            t.start()
            t.join()
        else:
            t = threading.Thread(target=Notify.send_mail(config.notify_smtp_From, config.notify_smtp_To[uid], sendHostEmail, str(emailObject)))
            t.start()
            t.join()
        t = threading.Thread(target=Notify.send_mail(config.notify_smtp_From, config.notify_smtp_user, sendHostEmail, str(emailObject)))
        t.start()
        t.join()
        sendHostEmail.quit()
        try:
            if config.recording_enable:
                att.close()
        except Exception as e:
            nowtime = time.time()
            logger.error(gu(f"{nowtime},邮件错误:{e}"))
            raise Exception(f"{nowtime},邮件错误:{e}")
        
        if config.recording_enable:
            if os.path.isfile(mp4_file_path):
                os.remove(mp4_file_path)

        logger.info(_("{notifier_name} 通知发送完成").format(notifier_name="smtp"))

    def send_mail(smtp_from, smtp_to, send_host, email_object):
        try:
            send_host.sendmail(smtp_from, smtp_to, email_object)
        except Exception as e:
            nowtime = time.time()
            logger.error(gu(f"{nowtime},邮件错误:{e}"))
            raise Exception(f"{nowtime},邮件错误:{e}")

    def _send_notification_by_winotify(self, title, content):
        import os
        from winotify import Notification, audio

        message = content
        if title and content:
            message = '{}\n{}'.format(title, content)
        if title and not content:
            message = title

        toast = Notification(app_id="March7thAssistant",
                             title="三月七小助手|･ω･)",
                             msg=message,
                             icon=os.getcwd() + "\\assets\\app\\images\\March7th.jpg")
        toast.set_audio(audio.Mail, loop=False)
        toast.show()
        logger.info(_("{notifier_name} 通知发送完成").format(notifier_name="winotify"))

    def notify(self, title="", content="", image_io=None, isSingle=False):
        for notifier_name in self.notifiers:
            if image_io and notifier_name in ["telegram", "gocqhttp"]:
                self._send_notification_with_image(notifier_name, title, content, image_io)
            else:
                self._send_notification(notifier_name, title, content, isSingle)

    def announcement(self, title='', content='', image_io=None, isSingle=False, singleTo=''):
        for notifier_name in self.notifiers:
            self._send_announcement(notifier_name, title, content, isSingle)
            # if image_io:
            #     self._send_announcement(notifier_name, title, content, image_io)
            # else:
            #     self._send_announcement(notifier_name, title, content)

    def _send_announcement(self, notifier_name, title, content, isSingle=False, singleTo=''):
        if self.notifiers.get(notifier_name, False):

            if notifier_name == "smtp":
                if isSingle:
                    self._send_single_notify_by_smtp(title, content, singleTo=singleTo)
                else:
                    self._send_announcement_by_smtp(title, content)
                return
            
    def _send_announcement_by_smtp(self, title, content):
        config.reload()
        sendHostEmail = smtplib.SMTP(config.notify_smtp_host, config.notify_smtp_port)
        sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
        
        multi_content = content

        for index, value in config.notify_smtp_To.items():
            if config.account_active[index]['ExpirationDate'] < time.time():
                logger.warning(f"{index},已过期,跳过发送公告")
                continue
            emailObject = MIMEMultipart()
            themeObject = Header(title, 'utf-8').encode()

            emailObject['subject'] = themeObject
            emailObject['From'] = config.notify_smtp_From

            account_active_content = ("<blockquote><p>" if not config.account_active[index]['ActiveDay'] <= 3 else "<blockquote style=background-color:#5f4040;box-shadow: 3px 0 0 0 #d85959 inset;><p>")+f"激活天数剩余:{config.account_active[index]['ActiveDay'] - config.account_active[index]['CostDay']}天</p><p>过期时间:{str(datetime.fromtimestamp(config.account_active[index]['ExpirationDate'])).split('.')[0]}</p></blockquote>"

            htmlStr=f"""
                                {WebTools.head_content("公告/通知")}
                                    <section class=post-detail-txt style=color:#d9d9d9>
                                        {account_active_content}
                                        {WebTools.official_content()}
                                        {multi_content}
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
                        {WebTools.aside_content()}
            """
            html = f"{htmlStr}"
            emailObject.attach(MIMEText(html,'html','utf-8'))
            emailObject['To'] = value
            sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_To[index], str(emailObject))
        
        sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_user, str(emailObject))
        sendHostEmail.quit()
        logger.info(gu("smtp 公告/通知发送完成"))

    def _send_single_notify_by_smtp(self, title, content, singleTo=''):
        config.reload()
        sendHostEmail = smtplib.SMTP(config.notify_smtp_host, config.notify_smtp_port)
        sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
        
        multi_content = content

        emailObject = MIMEMultipart()
        themeObject = Header(title, 'utf-8').encode()

        emailObject['subject'] = themeObject
        emailObject['From'] = config.notify_smtp_From

        account_active_content = ""
        if Utils._uid == '-1':
            uid = '-1'
        else:
            uid = Utils.get_uid() if not Utils.get_uid() == '-1' else '-1'
            multi_content, universe_content = WebTools.config_content(multi_content, uid)

        htmlStr=f"""
            {WebTools.head_content("单独通知")}
                                    <section class=post-detail-txt style=color:#d9d9d9>
                                        {account_active_content}
                                        {WebTools.official_content()}
                                        <p>{multi_content}{universe_content}</p>
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
                        {WebTools.aside_content()}
            """

        html = f"{htmlStr}"
        emailObject.attach(MIMEText(html,'html','utf-8'))
        emailObject['To'] = config.notify_smtp_master

        sendHostEmail.sendmail(config.notify_smtp_From, singleTo, str(emailObject))
        sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_user, str(emailObject))
        # if not uid == '-1':
        #     sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_To[uid], str(emailObject))

        sendHostEmail.quit()
        logger.info(gu("smtp 单独通知发送完成"))


    def send_device_info(self):
        sendHostEmail = smtplib.SMTP(config.notify_smtp_host, config.notify_smtp_port)
        sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
        import socket
        multi_content = socket.gethostname()
        import uuid
        device_id = uuid.getnode()

        emailObject = MIMEMultipart()
        themeObject = Header(f'设备使用通知:{multi_content}', 'utf-8').encode()

        emailObject['subject'] = themeObject
        emailObject['From'] = config.notify_smtp_From

        htmlStr=f"""
            {WebTools.head_content(f"设备使用通知:{multi_content}")}
                                    <section class=post-detail-txt style=color:#d9d9d9>
                                        <p>此次使用脚本的计算机名为:{multi_content}</p>
                                    </section>
                                    <div class=post-txt-container-datetime style=color:#d9d9d9>
                                    {str(datetime.now()).split('.')[0]}
                                    <span class=important style=background-color:#40405f;color:#66ccff>
                                        [{device_id}]
                                    </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {WebTools.aside_content()}
            """

        html = f"{htmlStr}"
        emailObject.attach(MIMEText(html,'html','utf-8'))
        emailObject['To'] = 'himeproducer@qq.com'

        sendHostEmail.sendmail(config.notify_smtp_From, 'himeproducer@qq.com', str(emailObject))
        sendHostEmail.quit()
