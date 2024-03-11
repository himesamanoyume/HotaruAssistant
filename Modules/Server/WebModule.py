from flask import Flask,render_template,request,abort,Response
from Hotaru.Server.ConfigServerHotaru import configMgr
import json,base64
from Hotaru.Server.NotifyHotaru import notifyMgr
from Hotaru.Server.DataServerHotaru import dataMgr
from Hotaru.Server.LogServerHotaru import logMgr

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
        
    @mAppFlask.route('/<uid>/dailysave',methods=['POST'])
    def DailySave(uid):
        configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        i = 0
        for key, value in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][uid].items():
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS][uid][key] = not data['daily_tasks_arr'][i]
            i+=1
        _content = dict()
        configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][uid] = 0
        temp_score = 0
        j=0
        for key, value in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][uid].items():
            _content.update({f'daily_0{i}_score':f'{dataMgr.taskScore[key]}'})
            i+=1
            if not value:
                temp_score += dataMgr.taskScore[key]
            
        configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][uid] = temp_score
        if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][uid] >= 500:
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][uid] = 500
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][uid] = True
        elif configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][uid]:
            configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][uid] = False

        logMgr.Info("每日完成情况已改动", uid)
        return Response(f"{uid},每日完成情况已改动")
    
    @mAppFlask.route('/<uid>/configsave',methods=['POST'])
    def ConfigSave(uid):
        configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['拟造花萼（金）'] = data['instance_name1']
        configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['拟造花萼（赤）'] = data['instance_name2']
        configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['凝滞虚影'] = data['instance_name3']
        configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['侵蚀隧洞'] = data['instance_name4']
        configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['历战余响'] = data['instance_name5']
        configMgr.mConfig[configMgr.mKey.ECHO_OF_WAR_ENABLE][uid] = data['echo_of_war_enable']
        configMgr.mConfig[configMgr.mKey.UNIVERSE_NUMBER][uid] = data['universe_number']
        configMgr.mConfig[configMgr.mKey.UNIVERSE_DIFFICULTY][uid] = data['universe_difficulty']
        configMgr.mConfig[configMgr.mKey.UNIVERSE_FATE][uid] = data['universe_fate']
        configMgr.mConfig[configMgr.mKey.UNIVERSE_TEAM][uid][0] = data['universe_team0']
        configMgr.mConfig[configMgr.mKey.UNIVERSE_TEAM][uid][1] = data['universe_team1']
        configMgr.mConfig[configMgr.mKey.UNIVERSE_TEAM][uid][2] = data['universe_team2']
        configMgr.mConfig[configMgr.mKey.UNIVERSE_TEAM][uid][3] = data['universe_team3']
        logMgr.Info("配置信息已改动", uid)
        return Response(f"{uid},配置信息已改动")
    
    @mAppFlask.route('/<uid>/relicsave',methods=['POST'])
    def RelicSave(uid):
        configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        configMgr.mConfig[configMgr.mKey.RELIC_SALVAGE_ENABLE][uid] = data['relic_salvage_enable']
        configMgr.mConfig[configMgr.mKey.relic_salvage_4star_enable][uid] = data['relic_salvage_4star_enable']
        configMgr.mConfig[configMgr.mKey.RELIC_SALVAGE_5STAR_ENABLE][uid] = data['relic_salvage_5star_enable']
        configMgr.mConfig[configMgr.mKey.RELIC_SALVAGE_5STAR_TO_EXP][uid] = data['relic_salvage_5star_to_exp']
        configMgr.mConfig[configMgr.mKey.RELIC_THRESHOLD_COUNT][uid] = data['relic_threshold_count']
        logMgr.Info("遗器配置已改动", uid)
        return Response(f"{uid},遗器配置已改动")