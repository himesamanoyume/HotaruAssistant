from flask import Flask,render_template,request,abort,Response
from Hotaru.Server.ConfigServerHotaru import configMgr
import json,base64
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
        noticeList, annList = WebModule.GetNoticeAndAnn()

        return render_template('index.html', loginList=WebModule.InitLoginList(), noticeList=noticeList, meta=dataMgr.meta, annList=annList, configMgr=configMgr)
    
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
    
    @mAppFlask.route('/activate')
    def Activate():
        configMgr.mConfigModule.ReloadConfig()
        noticeList, annList = WebModule.GetNoticeAndAnn()

        return render_template('activate.html', loginList=WebModule.InitLoginList(), configMgr=configMgr, noticeList=noticeList, annList=annList, url='activate')
    
    @staticmethod
    def GetNoticeAndAnn():
        noticeList = notifyMgr.CreateOfficialNotice()
        if noticeList:
            pass
        else:
            noticeList = [{"title":"未能获取到官方资讯,请刷新页面重试","day":"0","hour":"0", "start_time":"0","end_time":"0", "progress":1}]
        if dataMgr.YW5ub3VuY2VtZW50:
            annList = dataMgr.YW5ub3VuY2VtZW50
        else:
            annList = [{"Title":"{Y2NvbnRlbnR0}".format(Y2NvbnRlbnR0=base64.b64decode("5pyq6IO96I635Y+W5Yiw5YWs5ZGK").decode('utf-8')),"Content":"{Y2NvbnRlbnR0}".format(Y2NvbnRlbnR0=base64.b64decode("5pyq6IO96I635Y+W5Yiw5YWs5ZGK").decode('utf-8'))}]

        return noticeList, annList
    
    @mAppFlask.route('/register')
    def Register():
        configMgr.mConfigModule.ReloadConfig()
        noticeList, annList = WebModule.GetNoticeAndAnn()

        return render_template('register.html', loginList=WebModule.InitLoginList(), configMgr=configMgr, noticeList=noticeList, annList=annList, url='register', meta=dataMgr.meta)
        
        
            