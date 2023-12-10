from flask import Flask
from flask import render_template,request
import json
from module.config.config import Config


app = Flask(__name__)
loginList = list()

@app.route('/')
def index():
    loginList.clear()
    config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
    for index in range(len(config.multi_login_accounts)):
        uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
        loginList.append(f'{uidStr}')

    return render_template('index.html',loginList=loginList, config=config)

@app.route('/<uid>')
def config_setting(uid):
    config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
    with open("./assets/config/task_score_mappings.json", 'r', encoding='utf-8') as score_json:
        task_score = json.load(score_json)
        with open("./assets/config/ruby_detail.json", 'r', encoding='utf-8') as ruby_json:
            ruby = json.load(ruby_json)
            return render_template('config.html', uid=uid, config=config, ruby=ruby, task_score=task_score)

@app.route('/register')
def register():
    config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
    return render_template('register.html')

@app.route('/<uid>/save',methods=['POST'])
def config_save(uid):
    config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
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
    config.relic_salvage_enable[uid] = data['relic_salvage_enable']
    config.save_config()
    return ''


if __name__ == '__name__':
    #cmd: flask run --debug --host=0.0.0.0
    app.run(host='0.0.0.0')

def apprun():
    app.run(host='0.0.0.0')