from flask import Flask
from flask import render_template,request
import json
from module.config.config import Config


app = Flask(__name__)
loginList = list()
config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")

@app.route('/')
def index():
    loginList.clear()
    config.reload()
    for index in range(len(config.multi_login_accounts)):
        uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
        loginList.append(f'{uidStr}')
    return render_template('index.html',loginList=loginList, config=config)

@app.route('/<uid>')
def config_setting(uid):
    from datetime import datetime
    config.reload()
    with open("./assets/config/task_score_mappings.json", 'r', encoding='utf-8') as score_json:
        task_score = json.load(score_json)
        with open("./assets/config/ruby_detail.json", 'r', encoding='utf-8') as ruby_json:
            ruby = json.load(ruby_json)
            ActiveDate = str(datetime.fromtimestamp(config.account_active[uid]['ActiveDate'])).split('.')[0]
            ExpirationDate = str(datetime.fromtimestamp(config.account_active[uid]['ExpirationDate'])).split('.')[0]
            return render_template('config.html', uid=uid, config=config, ruby=ruby, task_score=task_score,ActiveDate=ActiveDate, ExpirationDate=ExpirationDate)

@app.route('/register')
def register():
    config.reload()
    with open("./assets/config/ruby_detail.json", 'r', encoding='utf-8') as ruby_json:
            ruby = json.load(ruby_json)
            return render_template('register.html',ruby=ruby)

@app.route('/<uid>/configsave',methods=['POST'])
def config_save(uid):
    config.reload()
    data = request.get_json('data')
    config.instance_type[uid] = data['instance_type']
    config.instance_names[uid]['拟造花萼（金）'] = data['instance_name1']
    config.instance_names[uid]['拟造花萼（赤）'] = data['instance_name2']
    config.instance_names[uid]['凝滞虚影'] = data['instance_name3']
    config.instance_names[uid]['侵蚀隧洞'] = data['instance_name4']
    config.instance_names[uid]['历战余响'] = data['instance_name5']
    config.echo_of_war_enable[uid] = data['echo_of_war_enable']
    config.universe_number[uid] = data['universe_number']
    config.universe_difficulty[uid] = data['universe_difficulty']
    config.universe_fate[uid] = data['universe_fate']
    config.universe_team[uid][0] = data['universe_team0']
    config.universe_team[uid][1] = data['universe_team1']
    config.universe_team[uid][2] = data['universe_team2']
    config.universe_team[uid][3] = data['universe_team3']
    config.relic_salvage_enable[uid] = data['relic_salvage_enable']
    config.save_config()
    return ''

@app.route('/register/save',methods=['POST'])
def register_save():
    config.reload()
    data = request.get_json('data')
    uid = data['reg_uid']
    config.want_register_accounts[uid] = {}
    config.want_register_accounts[uid]['email'] = data['email']
    config.want_register_accounts[uid]['reg_path'] = f"./reg/starrail-{uid}.reg"
    config.want_register_accounts[uid]['active_day'] = data['active_day']
    config.want_register_accounts[uid]['email'] = data['email']
    config.want_register_accounts[uid]['universe_team'] = {}
    tempList = list()
    tempList.append(data['universe_team0'])
    tempList.append(data['universe_team1'])
    tempList.append(data['universe_team2'])
    tempList.append(data['universe_team3'])
    config.want_register_accounts[uid]['universe_team'] = tempList
    config.want_register_accounts[uid]['universe_fate'] = data['universe_fate']
    config.want_register_accounts[uid]['universe_number'] = data['universe_number']
    config.want_register_accounts[uid]['universe_difficulty'] = data['universe_difficulty']
    config.save_config()
    return ''

@app.route('/smtpsave',methods=['POST'])
def smtp_save():
    config.reload()
    data = request.get_json('data')
    config.set_value("notify_smtp_enable", data['notify_smtp_enable'])
    config.set_value("notify_smtp_host", data['notify_smtp_host'])
    config.set_value("notify_smtp_user", data['notify_smtp_user'])
    config.set_value("notify_smtp_password", data['notify_smtp_password'])
    config.set_value("notify_smtp_From", data['notify_smtp_From'])
    config.set_value("notify_smtp_master", data['notify_smtp_master'])
    return ''

@app.route('/<uid>/activesave',methods=['POST'])
def active_save(uid):
    config.reload()
    data = request.get_json('data')
    if data['isWantActive']:
        config.account_active[uid]['isWantActive'] = data['isWantActive']
        config.account_active[uid]['ActiveDay'] = data['changeActiveDay']

    config.notify_smtp_To[uid] = data['notify_smtp_To']
    config.save_config()
    return ''

@app.route('/active')
def active():
    config.reload()
    return render_template('active.html',config=config)

@app.route('/active/alladd',methods=['POST'])
def all_active_save():
    config.reload()
    data = request.get_json('data')
    config.set_value("all_account_active_day", data['add_active_day'])
    return ''

@app.route('/notify')
def notify():
    loginList.clear()
    config.reload()
    for index in range(len(config.multi_login_accounts)):
        uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
        loginList.append(f'{uidStr}')
    return render_template('notify.html',config=config, loginList=loginList)

@app.route('/notify/announcement',methods=['POST'])
def announcement():
    config.reload()
    data = request.get_json('data')
    send_announcement(f"全体公告:{data['notify_title']}", f"<p>{data['notify_content']}</p>")
    return ''

@app.route('/notify/single',methods=['POST'])
def announcement_single():
    config.reload()
    data = request.get_json('data')
    send_announcement_single(f"单人通知:{data['notify_title']}", f"<p>{data['notify_content']}</p>", data['notify_single'], config.notify_smtp_To[data['notify_single']])
    return ''
            
if __name__ == '__name__':
    #cmd: flask run --debug --host=0.0.0.0
    app.run(host='0.0.0.0')

def apprun():
    app.run(host='0.0.0.0')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import random
import time
from datetime import datetime
version_txt = open("./assets/config/version.txt", "r", encoding='utf-8')
version = version_txt.read()
version_txt.close()
css = open("./assets/css/common.css", 'r', encoding='utf-8')
htmlStyle = css.read()
css.close()

def send_announcement(title, content):
    sendHostEmail = smtplib.SMTP(config.notify_smtp_host, config.notify_smtp_port)
    sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
    
    multi_content = content

    for index, value in config.notify_smtp_To.items():
        if config.account_active[index]['ExpirationDate'] < time.time():
            continue
        emailObject = MIMEMultipart()
        themeObject = Header(title, 'utf-8').encode()

        emailObject['subject'] = themeObject
        emailObject['From'] = config.notify_smtp_From

        account_active_content = ("<blockquote><p>" if not config.account_active[index]['ActiveDay'] <= 3 else "<blockquote style=background-color:#5f4040;box-shadow: 3px 0 0 0 #d85959 inset;><p>")+f"激活天数剩余:{config.account_active[index]['ActiveDay'] - config.account_active[index]['CostDay']}天</p><p>过期时间:{str(datetime.fromtimestamp(config.account_active[index]['ExpirationDate'])).split('.')[0]}</p></blockquote>"

        htmlStr=f"""
                            {head_content(title)}
                                <section class=post-detail-txt style=color:#d9d9d9>
                                    {account_active_content}
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
                    {aside_content()}
        """
        html = f"{htmlStr}"
        emailObject.attach(MIMEText(html,'html','utf-8'))
        emailObject['To'] = value
        sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_To[index], str(emailObject))
    
    sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_master, str(emailObject))
    sendHostEmail.quit()

def send_announcement_single(title, content, uid, singleTo=''):
    sendHostEmail = smtplib.SMTP(config.notify_smtp_host, config.notify_smtp_port)
    sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
    
    multi_content = content

    emailObject = MIMEMultipart()
    themeObject = Header(title, 'utf-8').encode()

    emailObject['subject'] = themeObject
    emailObject['From'] = config.notify_smtp_From

    account_active_content = ""
    multi_content, universe_content = config_content(multi_content, uid)

    htmlStr=f"""
        {head_content(title)}
                                <section class=post-detail-txt style=color:#d9d9d9>
                                    {account_active_content}
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
                    {aside_content()}
        """

    html = f"{htmlStr}"
    emailObject.attach(MIMEText(html,'html','utf-8'))
    emailObject['To'] = config.notify_smtp_single

    sendHostEmail.sendmail(config.notify_smtp_From, singleTo, str(emailObject))
    sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_user, str(emailObject))
    # if not uid == '-1':
    #     sendHostEmail.sendmail(config.notify_smtp_From, config.notify_smtp_To[uid], str(emailObject))

    sendHostEmail.quit()

def config_content(multi_content, uid):
    multi_content += f"<hr style=background:#d9d9d9><p><strong>配置详细</strong></p><div class=post-txt-container-datetime>该配置显示了当要挑战副本时会选择什么副本,如果配置与需求不符或需求有变化请和我说,然后我进行调整,否则我一律会首先遵照每个UID的配置来清体力</div>"
    multi_content += f"<p>清开拓力时将要打的副本类型:<span class=important style=background-color:#40405f;color:#66ccff>{config.instance_type[uid]}</span></p>"
    multi_content += f"<p>不同副本类型下的副本名称:</p>"

    with open("./assets/config/ruby_detail.json", 'r', encoding='utf-8') as ruby_json:
        ruby_mappings = json.load(ruby_json)

        nizaohuaejin_text = ''
        nizaohuaejin_text = ruby_mappings['拟造花萼（金）'][config.instance_names[uid]['拟造花萼（金）']]

        ningzhixuying_text = ''
        ningzhixuying_text = ruby_mappings['凝滞虚影'][config.instance_names[uid]['凝滞虚影']]

        qinshisuidong_text = ''
        qinshisuidong_text = ruby_mappings['侵蚀隧洞'][config.instance_names[uid]['侵蚀隧洞']]

        lizhanyuxiang_text = ''
        lizhanyuxiang_text = ruby_mappings['历战余响'][config.instance_names[uid]['历战余响']]

        multi_content += f"<p>拟造花萼（金）:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['拟造花萼（金）']}<rt class='ttt' style='background-color: unset;' data-rt='{nizaohuaejin_text}'></rt></ruby></span></p>"
        multi_content += f"<p>拟造花萼（赤）:<span class=important style=background-color:#40405f;color:#66ccff>{config.instance_names[uid]['拟造花萼（赤）']}</span></p>"
        multi_content += f"<p>凝滞虚影:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['凝滞虚影']}<rt class='ttt' style='background-color: unset;' data-rt='{ningzhixuying_text}'></rt></ruby></span></p>"
        multi_content += f"<p>侵蚀隧洞:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['侵蚀隧洞']}<rt class='ttt' style='background-color: unset;' data-rt='{qinshisuidong_text}'></rt></ruby></span></p>"
        multi_content += f"<p>是否清空3次历战余响:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if config.echo_of_war_enable[uid] else '否'}</span></p>"
        multi_content += f"<p>历战余响:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['历战余响']}<rt class='ttt' style='background-color: unset;' data-rt='{lizhanyuxiang_text}'></rt></ruby></span></p>"
        multi_content += f"<p>是否允许我分解4星及以下遗器:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if config.relic_salvage_enable[uid] else '否'}</span></p>"

        if config.universe_number[uid] in [3,4,5,6,7,8]:
            world_number = ruby_mappings['模拟宇宙'][str(config.universe_number[uid])]
            world_relic = ruby_mappings['模拟宇宙遗器'][str(config.universe_number[uid])]
        else:
            world_number = '世界选择有误'
            world_relic = ''

        universe_content = ''
        universe_content += f"<p>模拟宇宙:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{world_number}<rt class='ttt' style='background-color: unset;' data-rt='{world_relic}'></rt></ruby></span></p>"

        return multi_content, universe_content

def aside_content():
    aside_content = f"""
    <aside class=info-container>
                        <div class=info-container-inner id=info-container-inner>
                            <div class=info style=background-color:#2b2b2b>
                                <div class=fiximg style=width:100%;border-bottom-left-radius:0;border-bottom-right-radius:0;display:block>
                                    <div class=fiximg__container style=display:block;margin:0>
                                        <img class=info-icon loading=lazy src=https://blog.princessdreamland.top/usericon.webp style=margin-top:20px;max-height:185px;border-radius:3px;max-width:185px;width:100%;border:0;background-color:#66ccff>
                                    </div>
                                </div>
                                <div class=info-name style=color:#d9d9d9>
                                    <ruby>姫様の夢<rt class='ttt' data-rt='Ginka可爱捏'></rt></ruby>
                                </div>
                                <div class=info-txt style=color:#d9d9d9>
                                    Princess Dreamland
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
                    <a>HIMEPRODUCER</a> {version}
                </div>
            </footer>
        </div>
    """
    return aside_content

def head_content(contentTitle):
    randomNumber = random.randint(0,4)
    head_content = f"""
    <div class=body style=background-color:#3a3a3a>
        <style>{htmlStyle}</style>
            <header class=header style=position:sticky>
                <nav class=nav style='margin:0 15px;justify-content:center;background-color:#2b2b2b'>
                    <span class=blogName style=color:#d9d9d9 id=nav-index>
                        HIMEPRODUCER
                    </span>
                </nav>
            </header>
            <main class=main>
                <div class=home-container>
                    <div class=post-container style=margin:0;box-sizing:border-box;max-width:100%;width:100%;height:100%;border:0>
                        <div class=post style=background-color:#2b2b2b>
                            <div class=post-Img-container>
                                <img id=_index loading=lazy src=https://blog.princessdreamland.top/_index{randomNumber}.webp data-zoomable/>
                            </div>
                            <div class=post-txt-container>
                                <div class=post-txt-container-title style=color:#d9d9d9>
                                    <h4 style=color:#66ccff>
                                        {contentTitle}
                                    </h4>
                                </div>
                    """
    return head_content
