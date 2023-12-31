from flask import Flask,render_template,request
from module.config.config import Config
from tasks.daily.webtools import WebTools
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import random,json,requests,time,smtplib

app = Flask(__name__)
loginList = list()
config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
ts = open("./assets/config/task_score_mappings.json", 'r', encoding='utf-8')
task_score = json.load(ts)
ts.close()
rb = open("./assets/config/ruby_detail.json", 'r', encoding='utf-8')
ruby = json.load(rb)
rb.close()

def log(message, uid = -1):
    import datetime
    current_time = datetime.datetime.now()
    text = f"[{current_time.hour:02d}:{current_time.minute:02d}]\033[91m[{uid}]\033[0m|网页后台改动|{message}"
    print(text)

app.config['TEMPLATES_AUTO_RELOAD']=True
@app.template_filter('roundDate')
def roundDate(value):
    return round(value, 3)

app.config['TEMPLATES_AUTO_RELOAD']=True
@app.template_filter('universe_number')
def universe_number(value):
    return f"{value}"

@app.route('/')
def index():
    loginList.clear()
    config.reload()
    for index in range(len(config.multi_login_accounts)):
        uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
        loginList.append(f'{uidStr}')

    datalist = WebTools.official_notice()

    return render_template('index.html',loginList=loginList, config=config, datalist=datalist)

@app.route('/<uid>')
def config_setting(uid):
    from datetime import datetime
    config.reload()
    ActiveDate = str(datetime.fromtimestamp(config.account_active[uid]['ActiveDate'])).split('.')[0]
    ExpirationDate = str(datetime.fromtimestamp(config.account_active[uid]['ExpirationDate'])).split('.')[0]
    return render_template('config.html', uid=uid, config=config, ruby=ruby, task_score=task_score,ActiveDate=ActiveDate, ExpirationDate=ExpirationDate)
            

@app.route('/register')
def register():
    config.reload()
    return render_template('register.html',ruby=ruby)

@app.route('/<uid>/dailysave',methods=['POST'])
def daily_save(uid):
    config.reload()
    data = request.get_json('data')
    i = 0
    for key, value in config.daily_tasks[uid].items():
        config.daily_tasks[uid][key] = not data['daily_tasks_arr'][i]
        i+=1
    _content = dict()
    config.daily_tasks_score[uid] = 0
    temp_score = 0
    j=0
    for key, value in config.daily_tasks[uid].items():
        _content.update({f'daily_0{i}_score':f'{task_score[key]}'})
        i+=1
        if not value:
            temp_score += task_score[key]
        
    config.daily_tasks_score[uid] = temp_score
    if config.daily_tasks_score[uid] >= 500:
        config.daily_tasks_fin[uid] = True
    elif config.daily_tasks_fin[uid]:
        config.daily_tasks_fin[uid] = False
    config.save_config()
    log("每日完成情况已改动", uid)
    return ''

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
    log("配置信息已改动", uid)
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
    log("已完成注册", uid)
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
    log("SMTP服务设置已改动")
    return ''

@app.route('/miscsave',methods=['POST'])
def misc_save():
    config.reload()
    data = request.get_json('data')
    config.set_value("next_loop_time", data['next_loop_time'])
    config.set_value("hotkey_technique", data['hotkey_technique'])
    config.set_value("recording_enable", data['recording_enable'])
    config.set_value("hotkey_obs_start", data['hotkey_obs_start'])
    config.set_value("hotkey_obs_stop", data['hotkey_obs_stop'])
    log("杂项设置已改动")
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
    log("激活信息已改动并生效", uid)
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
    log("全体续期已生效")
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
    log("全体公告已发送")
    return ''

@app.route('/notify/single',methods=['POST'])
def announcement_single():
    config.reload()
    data = request.get_json('data')
    send_announcement_single(f"单人通知:{data['notify_title']}", f"<p>{data['notify_content']}</p>", data['notify_single'], config.notify_smtp_To[data['notify_single']])
    log("单人通知已发送")
    return ''

@app.route('/blacklist/append',methods=['POST'])
def append_blacklist():
    config.reload()
    data = request.get_json('data')
    uid = str(data['blacklist_uid'])
    if not uid in config.blacklist_uid:
        config.blacklist_uid.append(uid)

    config.save_config()
    log(f"黑名单已添加:{uid}")
    return ''

@app.route('/blacklist/remove',methods=['POST'])
def remove_blacklist():
    config.reload()
    data = request.get_json('data')
    uid = str(data['blacklist_uid'])
    if uid in config.blacklist_uid:
        if len(config.blacklist_uid) == 1:
            config.set_value("blacklist_uid", [])
        else:
            config.blacklist_uid.remove(uid)

    config.save_config()
    log(f"黑名单已移除:{uid}")
    return ''

@app.route('/cdkeylist/append',methods=['POST'])
def append_cdkeylist():
    config.reload()
    data = request.get_json('data')
    cdkey = data['cdkey_list']
    if not cdkey in config.cdkey_list:
        config.cdkey_list.append(cdkey)

    config.save_config()
    log(f"已添加兑换码:{cdkey}")
    return ''

@app.route('/cdkeylist/remove',methods=['POST'])
def remove_cdkeylist():
    config.reload()
    data = request.get_json('data')
    cdkey = data['cdkey_list']
    if cdkey in config.cdkey_list:
        if len(config.cdkey_list) == 1:
            config.set_value("cdkey_list", [])
        else:
            config.cdkey_list.remove(cdkey)

    config.save_config()
    log(f"已移除兑换码:{cdkey}")
    return ''
            
if __name__ == '__name__':
    #cmd: flask run --debug --host=0.0.0.0
    app.run(host='0.0.0.0')

def apprun():
    app.run(host='0.0.0.0')

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
                            {WebTools.head_content(title)}
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
    multi_content, universe_content = WebTools.config_content(multi_content, uid)

    htmlStr=f"""
        {WebTools.head_content(title)}
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
