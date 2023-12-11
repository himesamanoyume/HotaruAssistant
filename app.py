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
    config.save_config()
    return render_template('index.html',loginList=loginList, config=config)

@app.route('/<uid>')
def config_setting(uid):
    config.reload()
    with open("./assets/config/task_score_mappings.json", 'r', encoding='utf-8') as score_json:
        task_score = json.load(score_json)
        with open("./assets/config/ruby_detail.json", 'r', encoding='utf-8') as ruby_json:
            ruby = json.load(ruby_json)
            return render_template('config.html', uid=uid, config=config, ruby=ruby, task_score=task_score)

@app.route('/register')
def register():
    config.reload()
    with open("./assets/config/ruby_detail.json", 'r', encoding='utf-8') as ruby_json:
            ruby = json.load(ruby_json)
            return render_template('register.html',ruby=ruby)

@app.route('/<uid>/save',methods=['POST'])
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

@app.route('/active')
def active():
    config.reload()
    return render_template('active.html',config=config)
            
if __name__ == '__name__':
    #cmd: flask run --debug --host=0.0.0.0
    app.run(host='0.0.0.0')

def apprun():
    app.run(host='0.0.0.0')