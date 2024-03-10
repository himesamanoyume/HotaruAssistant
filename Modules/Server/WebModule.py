from flask import Flask,render_template,request,abort,Response
from Hotaru.Server.ConfigServerHotaru import configMgr
import json
from Hotaru.Server.NotifyHotaru import notifyMgr
from Hotaru.Server.DataServerHotaru import dataMgr

class WebModule:
    mAppFlask = Flask(__name__, static_folder='../../assets/static', static_url_path='', template_folder='../../assets/templates')

    mAppFlask.config['TEMPLATES_AUTO_RELOAD']=True
    @mAppFlask.template_filter('roundDate')
    def RoundDate(value):
        return round(value, 3)

    mAppFlask.config['TEMPLATES_AUTO_RELOAD']=True
    @mAppFlask.template_filter('universe_number')
    def UniverseNumber(value):
        return f"{value}"

    @mAppFlask.route('/')
    def Index():
        configMgr.mConfigModule.ReloadConfig()
        noticeList = notifyMgr.CreateOfficialNotice()

        return render_template('index.html', loginList=WebModule.InitLoginList(), noticeList=noticeList, meta=dataMgr.meta, annList=dataMgr.YW5ub3VuY2VtZW50, configMgr=configMgr)
    
    @staticmethod
    def InitLoginList():
        dataMgr.loginList.clear()
        for index in range(len(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS])):
            uidStr = str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index]).split('-')[1][:9]
            dataMgr.loginList.append(f'{uidStr}')

        return dataMgr.loginList
    
    @mAppFlask.route('/<uid>')
    def ConfigSetting(uid):
        configMgr.mConfigModule.ReloadConfig()
        return render_template('config.html', uid=uid, loginList=WebModule.InitLoginList(), configMgr=configMgr, taskScore=dataMgr.taskScore, meta=dataMgr.meta, len=len(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid]))
        
            