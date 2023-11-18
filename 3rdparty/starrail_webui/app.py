from flask import Flask
from managers.config_manager import config
from managers.config_manager import configM
from flask import render_template

app = Flask(__name__)
loginList = list()

@app.route('/')
def index():
    for index in range(len(config.multi_login_accounts)):
        uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
        loginList.append(f'{uidStr}')

    return render_template('index.html',loginList=loginList)

@app.route('/<uid>')
def config_setting(uid):
    return render_template('config.html', uid=uid)

@app.route('/<uid>/save',methods=['POST'])
def config_save():
    return "Saving!"


if __name__ == '__name__':
    app.debug=True
    app.run(host= '0.0.0.0')