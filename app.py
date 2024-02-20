from flask import Flask,render_template,request,abort,Response
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

def initLoginList():
    loginList.clear()
    for index in range(len(config.multi_login_accounts)):
        uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
        loginList.append(f'{uidStr}')

    return loginList


@app.route('/')
def index():
    config.reload()
    datalist = WebTools.official_notice()

    return render_template('index.html',loginList=initLoginList(), config=config, datalist=datalist, ruby=ruby, url='index')

@app.route('/<uid>')
def config_setting(uid):
    config.reload()
    return render_template('config.html', uid=uid, config=config, ruby=ruby, task_score=task_score, len=len(config.instance_type[uid]), loginList=initLoginList())
            

@app.route('/register')
def register():
    config.reload()
    return render_template('register.html',ruby=ruby, config=config, url='register',loginList=initLoginList())

@app.route('/activate')
def activate():
    config.reload()
    return render_template('activate.html', config=config, url='activate',loginList=initLoginList())

@app.route('/activate/save',methods=['POST'])
def activate_save():
    config.reload()
    data = request.get_json('data')
    uid = data['uid']
    if uid == '':
        abort(Response("uid不能为空"))
    if len(config.want_register_accounts) > 1:
        log("检测到有新注册表加入", uid)
        for uid, item in config.want_register_accounts.items():
            if uid == '111111111': continue
            if item['reg_path']=='':
                log("新的注册信息中注册表地址未完整填写",uid)
                abort(Response(f"{uid}:新的注册信息中注册表地址未完整填写"))
            if item['email']=='':
                log("新的注册信息中邮箱未完整填写", uid)
                abort(Response(f"{uid}:新的注册信息中邮箱未完整填写"))
            if not len(item['universe_team']) == 4:
                log("新的注册信息中模拟宇宙小队角色未填写满4人或超出4人", uid)
                abort(Response(f"{uid}:新的注册信息中模拟宇宙小队角色未填写满4人或超出4人"))
            if not item['universe_fate'] in [0,1,2,3,4,5,6,7,8]:
                log("新的注册信息中模拟宇宙命途不合法", uid)
                abort(Response(f"{uid}:新的注册信息中模拟宇宙命途不合法"))
            if not item['universe_number'] in [3,4,5,6,7,8]:
                log("新的注册信息中模拟宇宙选择的世界不合法", uid)
                abort(Response(f"{uid}:新的注册信息中模拟宇宙选择的世界不合法"))
            if not item['universe_difficulty'] in [1,2,3,4,5]:
                log("新的注册信息中模拟宇宙难度不合法", uid)
                abort(Response(f"{uid}:新的注册信息中模拟宇宙难度不合法"))

            if config.multi_login_accounts == {}:
                tempList = list()
                tempList.append(item['reg_path'])
                config.set_value("multi_login_accounts", tempList)
                config.save_config()
            else:
                config.multi_login_accounts.append(item['reg_path'])

            loginList.append(f"{str(item['reg_path'])}")
            config.notify_smtp_To[uid] = item['email']

            config.universe_number[uid] = item['universe_number']
            config.universe_difficulty[uid] = item['universe_difficulty']
            config.universe_fate[uid] = item['universe_fate']
            config.universe_team[uid] = item['universe_team']

            config.save_config()
            config.del_value('want_register_accounts', uid)
        log("注册表激活完成",uid)
        return Response(f"{uid},注册表激活完成!")
    else:
        log("未检测到有新注册表加入")
        return Response("未检测到有新注册表加入")
    

@app.route('/activate/del',methods=['POST'])
def activate_del():
    config.reload()
    data = request.get_json('data')
    uid = data['uid']
    config.del_value('want_register_accounts', uid)
    print("注册表删除成功")
    return Response("注册表删除成功")

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
        config.daily_tasks_score[uid] = 500
        config.daily_tasks_fin[uid] = True
    elif config.daily_tasks_fin[uid]:
        config.daily_tasks_fin[uid] = False
    config.save_config()
    log("每日完成情况已改动", uid)
    return Response(f"{uid},每日完成情况已改动")

@app.route('/<uid>/configsave',methods=['POST'])
def config_save(uid):
    config.reload()
    data = request.get_json('data')
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
    config.relic_salvage_4star_enable[uid] = data['relic_salvage_4star_enable']
    config.relic_salvage_5star_enable[uid] = data['relic_salvage_5star_enable']
    config.relic_salvage_5star_to_exp[uid] = data['relic_salvage_5star_to_exp']
    config.relic_threshold_count[uid] = data['relic_threshold_count']
    config.save_config()
    log("配置信息已改动", uid)
    return Response(f"{uid},配置信息已改动")

@app.route('/register/save',methods=['POST'])
def register_save():
    config.reload()
    data = request.get_json('data')
    uid = data['reg_uid']
    config.want_register_accounts[uid] = {}
    config.want_register_accounts[uid]['email'] = data['email']
    config.want_register_accounts[uid]['reg_path'] = f"./reg/starrail-{uid}.reg"
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
    return Response(f"{uid},已完成注册")

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
    return Response("SMTP服务设置已改动")

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
    return Response("杂项设置已改动")

@app.route('/notify')
def notify():
    config.reload()

    return render_template('notify.html',config=config, url='notify',loginList=initLoginList())

@app.route('/notify/announcement',methods=['POST'])
def announcement():
    config.reload()
    data = request.get_json('data')
    send_announcement(f"全体公告:{data['notify_title']}", f"<p>{data['notify_content']}</p>")
    log("全体公告已发送")
    return Response("全体公告已发送")

@app.route('/notify/single',methods=['POST'])
def announcement_single():
    config.reload()
    data = request.get_json('data')
    send_announcement_single(f"单人通知:{data['notify_title']}", f"<p>{data['notify_content']}</p>", data['notify_single'], config.notify_smtp_To[data['notify_single']])
    log("单人通知已发送")
    return Response("单人通知已发送")

@app.route('/instancelist/append',methods=['POST'])
def append_instance_list():
    config.reload()
    data = request.get_json('data')
    uid = str(data['uid'])
    add_instance_type = data['add_instance_type']

    config.instance_type[uid].append(add_instance_type)
    log(f"{uid},副本类型已添加:{add_instance_type}")

    config.save_config()
    return Response(f"{uid},副本类型已添加:{add_instance_type}")

@app.route('/instancelist/change',methods=['POST'])
def change_instance_list():
    config.reload()
    data = request.get_json('data')
    uid = str(data['uid'])
    add_instance_type = data['add_instance_type']
    change_instance_type_id = data['change_instance_type_id']
    change_instance = config.instance_type[uid][change_instance_type_id]

    config.instance_type[uid][change_instance_type_id] = add_instance_type
    config.save_config()
    log(f"{uid},副本类型已替换:{change_instance} → {add_instance_type}")
    
    return Response(f"{uid},副本类型已替换:{change_instance} → {add_instance_type}")

@app.route('/instancelist/remove',methods=['POST'])
def remove_instance_list():
    config.reload()
    data = request.get_json('data')
    uid = str(data['uid'])
    remove_instance_type_id = data['remove_instance_type_id']
    instance = config.instance_type[uid][remove_instance_type_id]
    if len(config.instance_type[uid]) == 1:
        abort(Response("不能再移除了"))
    else:
        config.instance_type[uid].remove(config.instance_type[uid][remove_instance_type_id])
        config.save_config()
        log(f"{uid}:{instance}已移除")
        return Response(f"{uid}:{instance}已移除")

@app.route('/blacklist/append',methods=['POST'])
def append_blacklist():
    config.reload()
    data = request.get_json('data')
    uid = str(data['blacklist_uid'])
    if not uid in config.blacklist_uid:
        config.blacklist_uid.append(uid)

    config.save_config()
    log(f"黑名单已添加:{uid}")
    return Response(f"黑名单已添加:{uid}")

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
    return Response(f"黑名单已移除:{uid}")

@app.route('/cdkeylist/append',methods=['POST'])
def append_cdkeylist():
    config.reload()
    data = request.get_json('data')
    cdkey = data['cdkey_list']
    if not cdkey in config.cdkey_list:
        config.cdkey_list.append(cdkey)

    config.save_config()
    log(f"已添加兑换码:{cdkey}")
    return Response(f"已添加兑换码:{cdkey}")

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
    return Response(f"已移除兑换码:{cdkey}")

@app.route('/borrowchar/append',methods=['POST'])
def append_borrowchar():
    config.reload()
    data = request.get_json('data')
    char = data['borrow_character']
    if not char in config.borrow_character:
        config.borrow_character.append(char)
        config.save_config()
        log(f"已添加助战角色:{ruby['角色'][char]}")
        return Response(f"已添加助战角色:{ruby['角色'][char]}")
    else:
        log(f"助战角色:{ruby['角色'][char]}已重复!")
        return Response(f"助战角色:{ruby['角色'][char]}已重复!")

@app.route('/borrowchar/remove',methods=['POST'])
def remove_borrowchar():
    config.reload()
    data = request.get_json('data')
    char = data['borrow_character']
    if char in config.borrow_character:
        if len(config.borrow_character) == 1:
            config.set_value("borrow_character", [])
        else:
            config.borrow_character.remove(char)

    config.save_config()
    log(f"已移除助战角色:{ruby['角色'][char]}")
    return Response(f"已移除助战角色:{ruby['角色'][char]}")
            
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
        emailObject = MIMEMultipart()
        themeObject = Header(title, 'utf-8').encode()

        emailObject['subject'] = themeObject
        emailObject['From'] = config.notify_smtp_From

        htmlStr=f"""
                            {WebTools.head_content(title)}
                                <section class=post-detail-txt style=color:#d9d9d9>
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

    multi_content, universe_content = WebTools.config_content(multi_content, uid)

    htmlStr=f"""
        {WebTools.head_content(title)}
                                <section class=post-detail-txt style=color:#d9d9d9>
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
