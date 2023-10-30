import base64
# coding=utf-8
import requests
from onepush import get_notifier
from managers.logger_manager import logger
from managers.config_manager import config
from tasks.daily.utils import Utils
from managers.translate_manager import _


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

    def _send_notification(self, notifier_name, title, content):
        if self.notifiers.get(notifier_name, False):

            if notifier_name == "winotify":
                self._send_notification_by_winotify(title, content)
                return

            if notifier_name == "pushplus":
                content = '.' if content is None or content == '' else content
            
            if notifier_name == "smtp":
                self._send_notification_by_smtp(title, content)
                return

            notifier_params = getattr(self, notifier_name, None)
            if notifier_params:
                n = get_notifier(notifier_name)
                try:
                    response = n.notify(**notifier_params,
                                        title=title, content=content)
                    logger.info(_("{notifier_name} 通知发送完成").format(
                        notifier_name=notifier_name.capitalize()))
                except Exception as e:
                    logger.error(_("{notifier_name} 通知发送失败").format(
                        notifier_name=notifier_name.capitalize()))
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

    def _send_notification_by_smtp(self, title, content):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.header import Header

        sendHostEmail = smtplib.SMTP_SSL(config.notify_smtp_host, config.notify_smtp_port)
        sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
        emailObject = MIMEMultipart()
        themeObject = Header(title, 'utf-8').encode()
        emailObject['subject'] = themeObject
        emailObject['From'] = config.notify_smtp_From
        emailObject['To'] = config.notify_smtp_To

        htmlStyle= "*{margin:0;padding:0;box-sizing:border-box;font-family:var(--code-font-family)}html{height:100%;scroll-behavior:smooth}img{transition-duration:.2s}.body{width:100%;min-height:100%;background-color:#3a3a3a;line-height:1.5;flex-direction:column;transition-duration:.15s;display:flex}@media screen and (max-width:990px){.home-container{flex-direction:column}.main>.home-container>.info-container{padding:0 15px;max-width:100%;position:inherit}.main>.home-container>.info-container>.info-container-inner{transform:rotateY(0);margin-top:5px}.main>.home-container>.info-container>.info-container-inner>.info{box-shadow:0 0 0 0 #000 inset,4px 4px 14px -13px #000}.main>.home-container>.info-container>.info-container-inner>.info-link{box-shadow:0 0 0 0 #000 inset,4px 4px 14px -13px #000}.main>.home-container>.info-container>.info-container-inner>.info>.fiximg>a>.info-icon{margin-top:20px;max-height:185px;border-radius:3px}.main>.home-container>.info-container>.info-container-inner>.info>.info-icon:hover{transform:translate3d(0,0,0)}.main>.home-container>.info-container>.info-container-inner>.info-link>.link-button{width:25%}.main>.home-container>.info-container>.info-container-inner>.info-link>.link-button:hover{transform:translate3d(0,0,0)}.main>.home-container>.post-container{max-width:100%;width:100%;padding:0 15px}.main>.home-container>.post-container>.main-post{box-shadow:4px 4px 14px -13px #000}.main>.home-container>.post-container>.post{box-shadow:0 0 0 0 #66ccff,4px 4px 14px -13px #000}.main>.home-container>.post-container>.post:hover{box-shadow:0 0 0 0 #66ccff,4px 4px 14px -13px #000}body>.topTitle{margin-top:5px;margin-bottom:5px;text-align:center;font-size:7vmax;color:#d9d9d9;width:100%;transition-duration:.2s;height:200px}body>.topTitle:hover{color:#66ccff}body>header>.nav{margin:0 15px}body>header>.nav>.blogName{padding:0;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none;width:0;font-size:25px;color:transparent}body>header>.nav>.nav-container{margin:0 auto;width:100%;display:inline-flex;display:-webkit-inline-flex;flex-wrap:wrap;justify-content:center}body>header>.nav>.nav-container>.nav-content>.nav-link{padding:0 5px;min-width:50px}body>header>.nav>.nav-container>.nav-content{width:50px}}::selection{background-color:#505074}::-moz-selection{background-color:#505074}@media(prefers-color-scheme:dark){body[data-theme=auto]{--body-bg:#3a3a3a;--footer-bg:#3a3a3abc;--post-bg:#2b2b2b;--header-bg:#262626;--post-shadow-color:#000;--text-color:#d9d9d9;--text-blogname-color:#ffffff;--page-button-color:#fff;--page-current-color:#717585;--tianyi-color:#66ccff;--post-code-bg:#333333;--post-code-text-color:snow;--post-reference-bg:#595959;--post-important-bg:#40405f;--code-block-bg:#272822;--selection-text-bg:#505074;--zh-font-family:Microsoft YaHei;--code-font-family:Menlo, Monaco, Consolas, Courier New, var(--zh-font-family), monospace}}@media(prefers-color-scheme:light){body[data-theme=auto]{--body-bg:rgb(235,235,235);--footer-bg:#ebebebbc;--post-bg:#fffafa;--header-bg:#c2c2c2;--post-shadow-color:#666699;--text-color:#666699;--text-blogname-color:#666699;--page-button-color:#474769;--page-current-color:#b1b6ce;--tianyi-color:#008ac5;--post-code-bg:#333333;--post-code-text-color:snow;--post-reference-bg:#595959;--post-important-bg:rgb(194,194,194);--selection-text-bg:rgb(177, 216, 221);--code-block-bg:#272822;--zh-font-family:PingFang SC, Hiragino Sans GB, Droid Sans Fallback, Microsoft YaHei;--code-font-family:Menlo, Monaco, Consolas, Courier New, var(--zh-font-family), monospace}}body[data-theme=dark]{--body-bg:#3a3a3a;--footer-bg:#3a3a3abc;--post-bg:#2b2b2b;--header-bg:#262626;--post-shadow-color:#000;--text-color:#d9d9d9;--text-blogname-color:#d9d9d9;--page-button-color:#fff;--page-current-color:#717585;--tianyi-color:#66ccff;--post-code-bg:#333333;--post-code-text-color:snow;--post-reference-bg:#595959;--post-important-bg:#40405f;--selection-text-bg:#686897;--code-block-bg:#272822;--zh-font-family:PingFang SC, Hiragino Sans GB, Droid Sans Fallback, Microsoft YaHei;--code-font-family:Menlo, Monaco, Consolas, Courier New, var(--zh-font-family), monospace}body[data-theme=light]{--body-bg:rgb(235,235,235);--footer-bg:#ebebebbc;--post-bg:#fffafa;--header-bg:#c2c2c2;--post-shadow-color:#666699;--text-color:#666699;--text-blogname-color:#666699;--page-button-color:#474769;--page-current-color:#b1b6ce;--tianyi-color:#008ac5;--post-code-bg:#333333;--post-code-text-color:snow;--post-reference-bg:#595959;--post-important-bg:rgb(194,194,194);--selection-text-bg:rgb(177, 216, 221);--code-block-bg:#272822;--zh-font-family:PingFang SC, Hiragino Sans GB, Droid Sans Fallback, Microsoft YaHei;--code-font-family:Menlo, Monaco, Consolas, Courier New, var(--zh-font-family), monospace}.main{display:block;flex:auto;min-height:300px;}.home-container{display:flex;display:-webkit-flex;margin:0 auto;width:100%;max-width:975px;word-break:break-all}.post-container{max-width:85%;width:775px;height:100%;border:0;padding:20px 20px 0 2px}input::-webkit-input-placeholder,textarea::-webkit-input-placeholder{font-size:13px;text-align:center}input:-moz-placeholder,textarea:-moz-placeholder{font-size:13px;text-align:center}input::-moz-placeholder,textarea::-moz-placeholder{font-size:13px;text-align:center}input:-ms-input-placeholder,textarea:-ms-input-placeholder{font-size:13px;text-align:center}.post{background-color:#2b2b2b;cursor:default;display:block;min-height:100px;width:100%;border:0;box-shadow:0 0 0 0 #66ccff,4px 4px 14px -13px #000}.newest-title{cursor:inherit;display:block;margin:75px 0;min-height:100px;width:100%;border:0;color:#d9d9d9;font-size:50px;text-align:center;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.chroma .lntd{line-height:23px;vertical-align:top;padding:0;margin:0;border:0}.chroma{background-color:var(--code-block-bg)}.post-page{border:0;background-color:#2b2b2b;width:100%;height:40px;box-shadow:4px 4px 14px -13px #000}.post-type{border:0;background-color:#2b2b2b;width:100%;height:40px}.post-page-container{height:40px;display:flex;display:-webkit-flex;justify-content:center;text-align:center}.post-page-container-currentPage{color:var(--page-current-color);line-height:40px;width:30px;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.post-page-container-content-left{height:40px;width:calc((100% - 27px)/2);justify-content:right;display:flex}.post-page-container-content-right{height:40px;width:calc((100% - 27px)/2);justify-content:left;display:flex}.post-page-container-button{cursor:pointer;color:#d9d9d9;justify-content:center;line-height:40px;width:30px;box-shadow:0 0 0 0 #66ccff inset;transition-duration:.2s}.post-page-container-button:hover{box-shadow:0 -2px 0 0 #66ccff inset;text-decoration:none}.post-page-container-nullSearch{padding:0 5px;color:#d9d9d9;justify-content:center;display:inline-block;line-height:40px;min-width:55px;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.main-post{text-align:center;background-color:#2b2b2b;backdrop-filter:blur(4px);display:block;cursor:inherit;min-height:400px;width:100%;border:0;cursor:default;color:#d9d9d9;box-shadow:4px 4px 14px -13px #000}.main-post img{width:100%;border:0}.main-post a{color:#66ccff}.important{background-color:#40405f;color:#66ccff;padding:0 3px}.highlight{background-color:var(--code-block-bg);color:#d9d9d9;position:relative;overflow:auto;max-height:400px}.highlight-wrapper:hover .copyCodeButton{opacity:1}.copyCodeButton{position:absolute;top:25px;right:25px;background:#40405f;border:none;padding:8px 16px;color:#d9d9d9;cursor:pointer;font-size:14px;opacity:0;transition:opacity .3s ease}.main-post-container{width:100%;display:inline-flex;justify-content:center;flex-wrap:wrap;-ms-flex-wrap:wrap;-webkit-flex-wrap:wrap}.main-post-content{text-align:left;margin:5px 20px}.main-post-content-txt{margin:8px 10px}a{text-decoration:none;color:#66ccff}a:hover{text-decoration:underline}.nav-content>a{color:#d9d9d9}.nav-index>a:hover{text-decoration:none}.post-Img-container{width:100%;max-height:200px;border:0;display:block;overflow-y:auto}::-webkit-scrollbar{height:auto}::-webkit-scrollbar-thumb{background-color:#40405f}::-webkit-scrollbar-corner{background-color:none}.post-Img-container img{width:100%;border:0;background-color:#66ccff;display:block}.post-txt-container{bottom:0;width:100%;cursor:default;min-height:60px;margin:0 0 10px}.post-txt-container-title{color:#d9d9d9;padding:15px 0 15px;display:inline-block}.post-txt-container-datetime{color:#d9d9d9;font-size:12px;line-height:30px;padding:0 20px;display:inline-block;transition-duration:.2s}.post-txt-container-datetime:hover{box-shadow:3px 0 0 0 #66ccff inset}.post-txt-container-introduction img{width:80%}pre{font-family:microsoft yahei ui;word-wrap:break-word;overflow:auto;word-break:break-all;word-wrap:break-word}.post-txt-container-title:hover{text-decoration: none;color:#66ccff}.post-txt-container .post-detail-txt p{margin-left:20px;margin-right:20px}.topTitle{margin:auto;text-align:center;font-size:10vmax;line-height:200px;color:#3a3a3a;width:100%;height:0;overflow:hidden;flex:none;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.errorTitle{margin:auto;text-align:center;font-size:15vmax;line-height:200px;color:#d9d9d9;width:100%;height:200px;overflow:hidden;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.errorDes{margin:auto;text-align:center;font-size:3vmax;color:#d9d9d9;width:100%;overflow:hidden;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.console-type-container{height:40px;padding:0 5px;display:flex;display:-webkit-flex;justify-content:center;text-align:center}.console-container-button{padding:0 5px;cursor:pointer;color:#fff;justify-content:center;line-height:40px;width:50px;box-shadow:0 0 0 0 #66ccff inset}.console-container-button:hover{box-shadow:0 -2px 0 0 #66ccff inset}ruby{text-indent:0}ruby>rt{display:block;font-size:50%;text-align:start}rt{text-indent:0;line-height:normal;-webkit-text-emphasis:none}rt.ttt::before{content:attr(data-rt)}hr{margin:40px auto;max-width:150px;width:30%;height:2px;opacity:.55;border:0;background:#d9d9d9;box-sizing:content-box;overflow:visible}.post-detail-txt .table-wrapper{overflow-x:auto;display:block;word-break:initial;padding:10px}.post-detail-txt{width:100%;color:#d9d9d9;padding:0 0 10px;line-height:30px;font-size:17px;word-break:break-word}.post-detail-txt a{color:#66ccff}.post-detail-txt p a{color:#66ccff}.post-detail-txt a:hover{text-decoration:underline}.post-detail-txt h1{font-size:42px;line-height:46px;box-shadow:0 -23px 0 0 #40405f inset}.post-detail-txt h2{font-size:36px;line-height:40px;box-shadow:0 -20px 0 0 #40405f inset}.post-detail-txt h3{font-size:32px;line-height:36px;box-shadow:0 -18px 0 0 #40405f inset}.post-detail-txt h4{font-size:26px;line-height:30px;box-shadow:0 -15px 0 0 #40405f inset}.post-detail-txt h5{font-size:24px;line-height:28px;box-shadow:0 -14px 0 0 #40405f inset}.post-detail-txt h6{font-size:20px;line-height:24px;box-shadow:0 -12px 0 0 #40405f inset}.post-detail-txt h1,.post-detail-txt h2,.post-detail-txt h3,.post-detail-txt h4,.post-detail-txt h5,.post-detail-txt h6{font-weight:500;margin:15px;word-break:break-word;width:fit-content}.post-detail-txt h1 code,.post-detail-txt h1 tt,.post-detail-txt h2 code,.post-detail-txt h2 tt,.post-detail-txt h3 code,.post-detail-txt h3 tt,.post-detail-txt h4 code,.post-detail-txt h4 tt,.post-detail-txt h5 code,.post-detail-txt h5 tt,.post-detail-txt h6 code,.post-detail-txt h6 tt{font-size:85%;font-family:var(--code-font-family)}.post-detail-txt>:first-child{margin-top:0}.post-detail-txt>:last-child{margin-bottom:0}.post-detail-txt blockquote{box-shadow:3px 0 0 0 #66ccff inset;background-color:#40405f;padding:10px 15px;color:#d9d9d9;font-size:inherit;border-left:2px solid var(--color-border)}.post-detail-txt p,.post-detail-txt ul,.post-detail-txt ol,.post-detail-txt dl,.post-detail-txt details{margin:10px}.post-detail-txt ul,.post-detail-txt ol{padding-left:28px;line-height:1.75}.post-detail-txt ul ul,.post-detail-txt ul ol,.post-detail-txt ol ol,.post-detail-txt ol ul{margin-top:0;margin-bottom:0;padding-left:16px}.post-detail-txt li>p{margin:0}.post-detail-txt .highlight pre code{font-family:var(--code-font-family);color:#fff}.post-detail-txt pre{word-wrap:normal;font-family:var(--code-font-family);background-color:var(--code-block-bg);padding:25px;overflow-x:auto;color:#fff}.post-detail-txt .highlight pre{margin-left:0;margin-right:0}.post-detail-txt kbd,.post-detail-txt code,.post-detail-txt tt{word-wrap:break-word;word-break:break-all;display:inline;font-family:var(--code-font-family);padding:2px 6px;color:#d9d9d9;background-color:#40405f;hyphens:none}.chroma .lntable{margin:0}pre.chroma{padding:5px}.post-detail-txt kbd br,.post-detail-txt code br,.post-detail-txt tt br{display:none}.post-detail-txt pre code{word-wrap:inherit;word-break:inherit;font-size:inherit;display:inline;padding:0;background-color:initial;hyphens:none;color:#fff;font-family:var(--code-font-family)}.post-detail-txt pre code br{display:unset;font-family:var(--code-font-family)}.post-detail-txt del code{text-decoration:inherit;font-family:var(--code-font-family)}mark{background-color:#40405f;color:#d9d9d9}.post-detail-txt blockquote>:first-child{margin-top:0}.post-detail-txt blockquote>:last-child{margin-bottom:0}.post-detail-txt .table-wrapper table{overflow-x:auto;border-collapse:collapse;background-color:initial}.post-detail-txt table tr{background-color:initial}.post-detail-txt table th{font-weight:500}.post-detail-txt table th,.post-detail-txt table td{background-color:initial;padding:4px 8px 4px 10px;border:1px solid #40405f;vertical-align:top}.post-detail-txt img:not(.emoji){max-width:100%;border:0;display:block}.post-detail-txt .footnotes{font-size:14px}.chroma .hl{display:block;width:100%;background-color:#ffc}.chroma .lnt{margin-right:.4em;padding:0 .4em;color:#7f7f7f;display:block}.chroma .ln{margin-right:.4em;padding:0 .4em;color:#7f7f7f}.chroma .k{color:#66d9ef}.chroma .kc{color:#66d9ef}.chroma .kd{color:#66d9ef}.chroma .kn{color:#f92672}.chroma .kp{color:#66d9ef}.chroma .kr{color:#66d9ef}.chroma .kt{color:#66d9ef}.chroma .n{color:#f8f8f2}.chroma .na{color:#a6e22e}.chroma .nb{color:#f8f8f2}.chroma .bp{color:#f8f8f2}.chroma .nc{color:#a6e22e}.chroma .no{color:#66d9ef}.chroma .nd{color:#a6e22e}.chroma .ni{color:#f8f8f2}.chroma .ne{color:#a6e22e}.chroma .nf{color:#a6e22e}.chroma .fm{color:#f8f8f2}.chroma .nl{color:#f8f8f2}.chroma .nn{color:#f8f8f2}.chroma .nx{color:#a6e22e}.chroma .py{color:#f8f8f2}.chroma .nt{color:#f92672}.chroma .nv{color:#f8f8f2}.chroma .vc{color:#f8f8f2}.chroma .vg{color:#f8f8f2}.chroma .vi{color:#f8f8f2}.chroma .vm{color:#f8f8f2}.chroma .l{color:#ae81ff}.chroma .ld{color:#e6db74}.chroma .s{color:#e6db74}.chroma .sa{color:#e6db74}.chroma .sb{color:#e6db74}.chroma .sc{color:#e6db74}.chroma .dl{color:#e6db74}.chroma .sd{color:#e6db74}.chroma .s2{color:#e6db74}.chroma .se{color:#ae81ff}.chroma .sh{color:#e6db74}.chroma .si{color:#e6db74}.chroma .sx{color:#e6db74}.chroma .sr{color:#e6db74}.chroma .s1{color:#e6db74}.chroma .ss{color:#e6db74}.chroma .m{color:#ae81ff}.chroma .mb{color:#ae81ff}.chroma .mf{color:#ae81ff}.chroma .mh{color:#ae81ff}.chroma .mi{color:#ae81ff}.chroma .il{color:#ae81ff}.chroma .mo{color:#ae81ff}.chroma .o{color:#f92672}.chroma .ow{color:#f92672}.chroma .p{color:#f8f8f2}.chroma .c{color:#75715e}.chroma .ch{color:#75715e}.chroma .cm{color:#75715e}.chroma .c1{color:#75715e}.chroma .cs{color:#75715e}.chroma .cp{color:#75715e}.chroma .cpf{color:#75715e}.chroma .gd{color:#f92672}.chroma .ge{font-style:italic}.chroma .gi{color:#a6e22e}.chroma .gs{font-weight:700}.chroma .gu{color:#75715e}@media screen and (max-width:990px){}header{display:block;flex:none;top:0;left:0;right:0;width:100%;margin:auto;z-index:9999;position:sticky}.nav{display:flex;display:-webkit-flex;top:0;min-height:60px;line-height:60px;color:#d9d9d9;box-shadow:0 6px 24px -14px #000000;background-color:#2b2b2b;min-height:60px}.blogName{padding:0 40px;font-size:23px;position:inherit;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none;color:#d9d9d9}.blogName:hover{color:#66ccff;text-decoration:none}.nav-container{display:flex;display:-webkit-flex}.nav-content{width:64px;height:60px;display:grid}.nav-link{padding:0 15px;cursor:pointer;text-align:center;justify-content:center;line-height:57px;min-width:64px}.nav-content:hover a .hover-bar{width:100%}.nav-link:hover{color:#66ccff;text-decoration:none}.hover-bar-active{color:#66ccff;text-decoration:none;width:100%;margin:0 auto;height:3px;background-color:#66ccff;transition-duration:.3s;box-shadow:0 -5px 25px 1px #66ccff}.hover-bar{width:0;margin:0 auto;height:3px;background-color:#66ccff;transition-duration:.3s;box-shadow:0 -5px 25px 1px #66ccff}.footer{width:100%;padding:40px 0 20px;background-color:#3a3a3abc;backdrop-filter:blur(4px);color:#d9d9d9;display:inline-flex;text-align:center;justify-content:space-around;flex-wrap:wrap;-ms-flex-wrap:wrap;-webkit-flex-wrap:wrap;flex:none}.footer-content{line-height:20px;font-size:10px;padding:0 20px}.footer>.footer-content>a{min-width:168px}.info-container{max-width:21%;padding:20px 0 5px 20px;top:60px;height:100%;position:sticky;perspective:1500px;-webkit-perspective:1500px}.info-container-inner{height:100%;transform:rotateY(-20deg)}.info{text-align:center;backdrop-filter:blur(4px);border:0;background-color:#2b2b2b;width:100%;margin-top:10px;box-shadow:2px 1px 11px -10px #000}.info-icon{max-width:185px;margin-top:1px;width:100%;border:0;background-color:#66ccff}.info-icon:hover{transform:translate3d(-5px,-5px,0)}.info-name{font-size:25px;line-height:50px;width:100%;color:#d9d9d9}.info-txt{word-break: break-word;font-size:15px;line-height:25px;width:100%;color:#d9d9d9}.info-link{backdrop-filter:blur(4px);display:inline-flex;flex-wrap:wrap;border:0;background-color:#2b2b2b;width:100%;min-height:40px;margin-top:10px;justify-content:space-around;box-shadow:2px 1px 11px -10px #000}.link-button{border:0;width: 20%;text-align:center;cursor:pointer;transition-duration:.2s;box-shadow:0 0 0 0 #66ccff inset;justify-content:center}.link-button:hover{box-shadow:0 -2px 0 0 #66ccff inset;transform:translate3d(-5px,-5px,0)}.searchBar{height:46.75px;width:80%;font-size:18px;padding:0 10px;border:0;color:#d9d9d9;background-color:#2b2b2b}.searchBar:focus{outline:none}.searchButton{height:46.75px;width:20%;position:relative;text-align:center;cursor:pointer;font-size:15px;color:#d9d9d9;box-shadow:0 0 0 0 #66ccff inset;transition-duration:.2s}.searchButton:hover{box-shadow:0 -2px 0 0 #66ccff inset}.post-detail-dynamic{color:#d9d9d9;height:40px;line-height:40px;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.post-detail-datetime{color:#d9d9d9;height:40px;line-height:40px;user-select:none;-moz-user-select:none;-ms-user-select:none;-webkit-user-select:none}.post-detail-title{width:100%;text-align:center;padding:30px 0;font-size:40px;color:#d9d9d9}.post-detail-postInfo-container{width:100%;display:flex;display:-webkit-flex;justify-content:space-around}.highlight-wrapper{position:relative}.mywaifu{position:relative}.mywaifu img{position:absolute;left:0;bottom:0}.post-txt-container-title h1,.post-txt-container-title h2,.post-txt-container-title h3,.post-txt-container-title h4,.post-txt-container-title h5,.post-txt-container-title h6{font-weight:500;padding:0 20px 0 20px;font-size:28px;line-height:45px;transition-duration:.2s}.post-txt-container-title:hover > h1,.post-txt-container-title:hover > h2,.post-txt-container-title:hover > h3,.post-txt-container-title:hover > h4,.post-txt-container-title:hover > h5,.post-txt-container-title:hover > h6{box-shadow:3px 0 0 0 #66ccff inset,950px 0 0 0 #40405f inset}"

        new_power = Utils._content['new_power']
        uid = Utils._content['uid']
        date = Utils._content['date']
        date = str(date).split('.')[0]
        full_power_time = Utils._content['full_power_time']
        full_power_time = str(full_power_time).split('.')[0]
        multi_content = Utils._content['multi_content']
        multi_content += f"<p><strong>每日完成情况</strong></p>"

        for i in range(5):
            multi_content += f"<p>{Utils._content[f'daily_0{i+1}']}:<span class=important>"+(f"未完成</span></p>" if Utils._content[f'daily_0{i+1}_value'] else "已完成</span></p>")

        multi_content += f"<p><strong>当前活跃度</strong></p><blockquote><p>{Utils._content['daily_tasks_score']}/500</p></blockquote>"
        multi_content += f"<p><strong>当前模拟宇宙积分</strong></p><blockquote><p>{Utils._content['current_universe_score']}/{Utils._content['max_universe_score']}</p></blockquote>"
        multi_content += f"<p><strong>预计满体力时间</strong></p><blockquote><p>{full_power_time}</p></blockquote>"

        multi_content += f"<hr><p><strong>配置详细</strong></p><div class=post-txt-container-datetime>如果配置与需求不符要跟我说</div>"
        multi_content += f"<p>日常完成后清体力时应选择的副本类型:{config.instance_type[uid]}</p>"
        multi_content += f"<p>不同类型下的副本名称:</p>"
        multi_content += f"<p>拟造花萼（金）:{config.instance_names[uid]['拟造花萼（金）']}</p>"
        multi_content += f"<p>拟造花萼（赤）:{config.instance_names[uid]['拟造花萼（赤）']}</p>"
        multi_content += f"<p>凝滞虚影:{config.instance_names[uid]['凝滞虚影']}</p>"
        multi_content += f"<p>侵蚀隧洞:{config.instance_names[uid]['侵蚀隧洞']}</p>"
        multi_content += f"<p>历战余响:{config.instance_names[uid]['历战余响']}</p><hr>"

        multi_content += f"<blockquote><strong>查表</strong>"
        multi_content += f"<p>拟造花萼（金）:</p><p>无,回忆之蕾（角色经验）,以太之蕾（武器经验）,藏珍之蕾（信用点）</p>"
        multi_content += f"<p>拟造花萼（赤）:</p><p>无,毁灭之蕾,存护之蕾,巡猎之蕾,丰饶之蕾,智识之蕾,同谐之蕾,虚无之蕾</p>"
        multi_content += f"<p>凝滞虚影:</p><p>无,空海之形,巽风之形,鸣雷之形,炎华之形,锋芒之形,霜晶之形,幻光之形,冰棱之形,震厄之形,偃偶之形,孽兽之形,天人之形,燔灼之形</p>"
        multi_content += f"<p><p>侵蚀隧洞:</p><p>无,霜风之径,迅拳之径,漂泊之径,睿治之径,圣颂之径,野焰之径,药使之径</p>"
        multi_content += f"<p>历战余响:</p><p>无,毁灭的开端,寒潮的落幕,不死的神实</p></blockquote>"
        
        htmlStr=f"<div class=body><header class=header><nav class=nav><span class=blogName id=nav-index title=首页>HIMEPRODUCER</span><div class=nav-container><div class=nav-content></div></div></nav></header><main class=main><div class=home-container><div class=post-container><div class=post><div class=post-Img-container></div><div class=post-txt-container><div class=post-txt-container-title><h4>普罗丢瑟代练</h4></div><section class=post-detail-txt><p><strong>体力去向:</strong>下号时体力:{new_power}</p>{multi_content}</section><div class=post-txt-container-datetime>{date} <span class=important>[{uid}]</span></div></div></div></div><aside class=info-container><div class=info-container-inner id=info-container-inner><div class=info><div class=fiximg style=width:100%;border-bottom-left-radius:0;border-bottom-right-radius:0;display:block><a href=/ class=fiximg__container style=display:block;margin:0><img class=info-icon loading=lazy src=https://blog.princessdreamland.top/usericon.webp title=头像></a></div><div class=info-name>姫様の夢</div><div class=info-txt>Princess Dreamland</div></div></div></aside></div></main><footer class=footer><div class=footer-content>Copyright © 2021-2023 @姫様の夢/公主殿下的梦境</div><div class=footer-content><a>HIMEPRODUCER</a> Ver1.0</div></footer></div>"


        html=f"<style>{htmlStyle}</style>{htmlStr}"
        emailObject.attach(MIMEText(html,'html','utf-8'))

        sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_To, str(emailObject))
        sendHostEmail.quit()
        logger.info(_("{notifier_name} 通知发送完成").format(notifier_name="smtp"))

    
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

    def notify(self, title="", content="", image_io=None):
        for notifier_name in self.notifiers:
            if image_io and notifier_name in ["telegram", "gocqhttp"]:
                self._send_notification_with_image(notifier_name, title, content, image_io)
            else:
                self._send_notification(notifier_name, title, content)
