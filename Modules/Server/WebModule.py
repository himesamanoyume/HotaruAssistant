from flask import Flask,render_template,request,abort,Response
from Hotaru.Server.ConfigServerHotaru import configMgr
import json,base64
from Hotaru.Server.NotifyHotaru import notifyMgr
from Hotaru.Server.DataServerHotaru import dataMgr
from Hotaru.Server.LogServerHotaru import logMgr
from Modules.Utils.InitUidConfig import InitUidConfig

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
        # configMgr.mConfigModule.ReloadConfig()
        noticeList, annList = WebModule.GetNoticeAndAnn()

        return render_template(
            'index.html',
            loginList=WebModule.InitLoginList(),
            noticeList=noticeList,
            dataMgr=dataMgr,
            annList=annList,
            configMgr=configMgr,
            updateList=notifyMgr.CreateUpdateContent(dataMgr)
            )
    
    @staticmethod
    def InitLoginList():
        dataMgr.loginList.clear()
        for index in range(len(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS])):
            uidStr = str(configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS][index]).split('-')[1][:9]
            dataMgr.loginList.append(f'{uidStr}')

        return dataMgr.loginList
    
    @mAppFlask.route('/<uid>')
    def ConfigSetting(uid):
        # configMgr.mConfigModule.ReloadConfig()
        noticeList, annList = WebModule.GetNoticeAndAnn()

        return render_template(
            'config.html', 
            uid=uid, 
            loginList=WebModule.InitLoginList(),
            configMgr=configMgr,
            updateList=notifyMgr.CreateUpdateContent(dataMgr),
            annList=annList,
            dataMgr=dataMgr, 
            len=len(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid])
            )
    
    @mAppFlask.route('/activate')
    def Activate():
        # configMgr.mConfigModule.ReloadConfig()
        noticeList, annList = WebModule.GetNoticeAndAnn()

        return render_template(
            'activate.html', 
            loginList=WebModule.InitLoginList(),
            configMgr=configMgr,
            dataMgr=dataMgr,
            noticeList=noticeList, 
            annList=annList, 
            url='activate',
            updateList=notifyMgr.CreateUpdateContent(dataMgr)
            )
    
    @staticmethod
    def GetNoticeAndAnn():
        noticeList = notifyMgr.CreateOfficialNotice()
        annList = notifyMgr.CreateAnnList(dataMgr)

        return noticeList, annList
    
    @mAppFlask.route('/register')
    def Register():
        # configMgr.mConfigModule.ReloadConfig()
        noticeList, annList = WebModule.GetNoticeAndAnn()

        return render_template(
            'register.html', 
            loginList=WebModule.InitLoginList(), 
            configMgr=configMgr,
            dataMgr=dataMgr,
            noticeList=noticeList, 
            annList=annList, 
            url='register',
            updateList=notifyMgr.CreateUpdateContent(dataMgr)
            )
        
    @mAppFlask.route('/<uid>/dailysave',methods=['POST'])
    def DailySave(uid):
        # configMgr.mConfigModule.ReloadConfig()
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

        logMgr.Info(f"{uid},每日完成情况已改动")
        return Response(f"{uid},每日完成情况已改动")
    
    @mAppFlask.route('/<uid>/configsave',methods=['POST'])
    def ConfigSave(uid):
        # configMgr.mConfigModule.ReloadConfig()
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
        logMgr.Info(f"{uid},配置信息已改动")
        return Response(f"{uid},配置信息已改动")
    
    @mAppFlask.route('/<uid>/configmiscsave',methods=['POST'])
    def ConfigMiscSave(uid):
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_ENABLE][uid] = data['instance_team_enable']
        configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid] = data['instance_team_number']
        configMgr.mConfig[configMgr.mKey.USE_RESERVED_TRAILBLAZE_POWER][uid] = data['use_reserved_trailblaze_power']
        configMgr.mConfig[configMgr.mKey.USE_FUEL][uid] = data['use_fuel']
        configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER_ENABLE][uid] = data['borrow_character_enable']
        configMgr.mConfig[configMgr.mKey.NOTIFY_SMTP_TO][uid] = data['notify_smtp_To']
        logMgr.Info(f"{uid},杂项配置已改动")
        return Response(f"{uid},杂项配置已改动")
    
    @mAppFlask.route('/<uid>/relicsave',methods=['POST'])
    def RelicSave(uid):
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        configMgr.mConfig[configMgr.mKey.RELIC_SALVAGE_ENABLE][uid] = data['relic_salvage_enable']
        configMgr.mConfig[configMgr.mKey.RELIC_SALVAGE_4STAR_ENABLE][uid] = data['relic_salvage_4star_enable']
        configMgr.mConfig[configMgr.mKey.RELIC_SALVAGE_5STAR_ENABLE][uid] = data['relic_salvage_5star_enable']
        configMgr.mConfig[configMgr.mKey.RELIC_SALVAGE_5STAR_TO_EXP][uid] = data['relic_salvage_5star_to_exp']
        configMgr.mConfig[configMgr.mKey.RELIC_THRESHOLD_COUNT][uid] = data['relic_threshold_count']
        logMgr.Info(f"{uid},遗器配置已改动")
        return Response(f"{uid},遗器配置已改动")
    
    @mAppFlask.route('/register/save',methods=['POST'])
    def RegisterSave():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = data['reg_uid']
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid] = {}
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['email'] = data['email']
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['reg_path'] = f"./reg/starrail-{uid}.reg"
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['email'] = data['email']
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['universe_team'] = {}
        tempList = list()
        tempList.append(data['universe_team0'])
        tempList.append(data['universe_team1'])
        tempList.append(data['universe_team2'])
        tempList.append(data['universe_team3'])
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['universe_team'] = tempList
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['universe_fate'] = data['universe_fate']
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['universe_number'] = data['universe_number']
        configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS][uid]['universe_difficulty'] = data['universe_difficulty']
        logMgr.Info(f"{uid},已完成注册")
        return Response(f"{uid},已完成注册")
    
    @mAppFlask.route('/activate/save',methods=['POST'])
    def ActivateSave():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = data['uid']
        if uid == '':
            abort(Response("uid不能为空"))
        if len(configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS]) > 1:
            logMgr.Info(f"{uid}:检测到有新注册表加入")
            for uid, item in configMgr.mConfig[configMgr.mKey.WANT_REGISTER_ACCOUNTS].items():
                if uid == '111111111': continue
                if item['reg_path']=='':
                    logMgr.Warning(f"{uid}:新的注册信息中注册表地址未完整填写",uid)
                    abort(Response(f"{uid}:新的注册信息中注册表地址未完整填写"))
                if item['email']=='':
                    logMgr.Warning(f"{uid}:新的注册信息中邮箱未完整填写")
                    abort(Response(f"{uid}:新的注册信息中邮箱未完整填写"))
                if not len(item['universe_team']) == 4:
                    logMgr.Warning(f"{uid}:新的注册信息中模拟宇宙小队角色未填写满4人或超出4人")
                    abort(Response(f"{uid}:新的注册信息中模拟宇宙小队角色未填写满4人或超出4人"))
                if not item['universe_fate'] in [0,1,2,3,4,5,6,7,8]:
                    logMgr.Warning(f"{uid}:新的注册信息中模拟宇宙命途不合法")
                    abort(Response(f"{uid}:新的注册信息中模拟宇宙命途不合法"))
                if not item['universe_number'] in [3,4,5,6,7,8]:
                    logMgr.Warning(f"{uid}:新的注册信息中模拟宇宙选择的世界不合法")
                    abort(Response(f"{uid}:新的注册信息中模拟宇宙选择的世界不合法"))
                if not item['universe_difficulty'] in [1,2,3,4,5]:
                    logMgr.Warning(f"{uid}:新的注册信息中模拟宇宙难度不合法")
                    abort(Response(f"{uid}:新的注册信息中模拟宇宙难度不合法"))

                if configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS] == {}:
                    tempList = list()
                    tempList.append(item['reg_path'])
                    configMgr.mConfig.SetValue(configMgr.mKey.MULTI_LOGIN_ACCOUNTS, tempList)
                else:
                    configMgr.mConfig[configMgr.mKey.MULTI_LOGIN_ACCOUNTS].append(item['reg_path'])

                dataMgr.loginList.append(f"{str(item['reg_path'])}")
                configMgr.mConfig[configMgr.mKey.NOTIFY_SMTP_TO][uid] = item['email']

                configMgr.mConfig[configMgr.mKey.UNIVERSE_NUMBER][uid] = item['universe_number']
                configMgr.mConfig[configMgr.mKey.UNIVERSE_DIFFICULTY][uid] = item['universe_difficulty']
                configMgr.mConfig[configMgr.mKey.UNIVERSE_FATE][uid] = item['universe_fate']
                configMgr.mConfig[configMgr.mKey.UNIVERSE_TEAM][uid] = item['universe_team']

                InitUidConfig.InitUidDefaultConfig(configMgr, logMgr, uid)

                configMgr.mConfig.DelValue(configMgr.mKey.WANT_REGISTER_ACCOUNTS, uid)
            logMgr.Info(f"{uid},注册表激活完成")
            return Response(f"{uid},注册表激活完成!")
        else:
            logMgr.Warning("未检测到有新注册表加入")
            return Response("未检测到有新注册表加入")
    
    @mAppFlask.route('/activate/del',methods=['POST'])
    def activate_del():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = data['uid']
        configMgr.mConfig.DelValue(configMgr.mKey.WANT_REGISTER_ACCOUNTS, uid)
        logMgr.Info("注册表删除成功")
        return Response("注册表删除成功")
    
    @mAppFlask.route('/smtpsave',methods=['POST'])
    def SmtpSave():
        # # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        configMgr.mConfig.SetValue(configMgr.mKey.NOTIFY_SMTP_ENABLE, data['notify_smtp_enable'])
        configMgr.mConfig.SetValue(configMgr.mKey.NOTIFY_SMTP_HOST, data['notify_smtp_host'])
        configMgr.mConfig.SetValue(configMgr.mKey.NOTIFY_SMTP_USER, data['notify_smtp_user'])
        configMgr.mConfig.SetValue(configMgr.mKey.NOTIFY_SMTP_PASSWORD, data['notify_smtp_password'])
        configMgr.mConfig.SetValue(configMgr.mKey.NOTIFY_SMTP_FROM, data['notify_smtp_From'])
        configMgr.mConfig.SetValue(configMgr.mKey.NOTIFY_SMTP_MASTER, data['notify_smtp_master'])
        logMgr.Info("SMTP服务设置已改动")
        return Response("SMTP服务设置已改动")
    
    @mAppFlask.route('/miscsave',methods=['POST'])
    def MiscSave():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        configMgr.mConfig.SetValue(configMgr.mKey.CHECK_UPDATE, data['check_update'])
        configMgr.mConfig.SetValue(configMgr.mKey.CHECK_PRERELEASE_UPDATE, data['check_prerelease_update'])
        configMgr.mConfig.SetValue(configMgr.mKey.DEV_SCREEN_ENABLE, data['dev_screen_enable'])
        configMgr.mConfig.SetValue(configMgr.mKey.NEXT_LOOP_TIME, data['next_loop_time'])
        configMgr.mConfig.SetValue(configMgr.mKey.HOTKEY_TECHNIQUE, data['hotkey_technique'])
        configMgr.mConfig.SetValue(configMgr.mKey.DAILY_HIMEKO_TRY_ENABLE, data['daily_himeko_try_enable'])
        configMgr.mConfig.SetValue(configMgr.mKey.RECORDING_ENABLE, data['recording_enable'])
        configMgr.mConfig.SetValue(configMgr.mKey.HOTKEY_OBS_START, data['hotkey_obs_start'])
        configMgr.mConfig.SetValue(configMgr.mKey.HOTKEY_OBS_STOP, data['hotkey_obs_stop'])
        logMgr.Info("杂项设置已改动")
        return Response("杂项设置已改动")
    
    @mAppFlask.route('/instancelist/change',methods=['POST'])
    def ChangeInstanceList():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = str(data['uid'])
        addInstanceType = data['add_instance_type']
        changeInstanceTypeId = data['change_instance_type_id']
        changeInstance = configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid][changeInstanceTypeId]

        configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid][changeInstanceTypeId] = addInstanceType
        logMgr.Info(f"{uid},副本类型已替换:{changeInstance} → {addInstanceType}")
        
        return Response(f"{uid},副本类型已替换:{changeInstance} → {addInstanceType}")
    
    @mAppFlask.route('/instancelist/append',methods=['POST'])
    def AppendInstanceList():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = str(data['uid'])
        addInstanceType = data['add_instance_type']

        configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid].append(addInstanceType)
        logMgr.Info(f"{uid},副本类型已添加:{addInstanceType}")

        return Response(f"{uid},副本类型已添加:{addInstanceType}")
    
    @mAppFlask.route('/instancelist/remove',methods=['POST'])
    def RemoveInstanceList():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = str(data['uid'])
        removeInstanceTypeId = data['remove_instance_type_id']
        instance = configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid][removeInstanceTypeId]
        if len(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid]) == 1:
            abort(Response("不能再移除了"))
        else:
            configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid].remove(configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid][removeInstanceTypeId])
            logMgr.Info(f"{uid}:{instance}已移除")
            return Response(f"{uid}:{instance}已移除")
        
    @mAppFlask.route('/blacklist/append',methods=['POST'])
    def AppendBlacklist():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = str(data['blacklist_uid'])
        if not uid in configMgr.mConfig[configMgr.mKey.BLACKLIST_UID]:
            configMgr.mConfig[configMgr.mKey.BLACKLIST_UID].append(uid)

        logMgr.Info(f"黑名单已添加:{uid}")
        return Response(f"黑名单已添加:{uid}")

    @mAppFlask.route('/blacklist/remove',methods=['POST'])
    def RemoveBlacklist():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        uid = str(data['blacklist_uid'])
        if uid in configMgr.mConfig[configMgr.mKey.BLACKLIST_UID]:
            if len(configMgr.mConfig[configMgr.mKey.BLACKLIST_UID]) == 1:
                configMgr.mConfig.SetValue(configMgr.mKey.BLACKLIST_UID, [])
            else:
                configMgr.mConfig[configMgr.mKey.BLACKLIST_UID].remove(uid)

        logMgr.Info(f"黑名单已移除:{uid}")
        return Response(f"黑名单已移除:{uid}")

    @mAppFlask.route('/cdkeylist/append',methods=['POST'])
    def AppendCdkeylist():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        cdkey = data['cdkey_list']
        if not cdkey in configMgr.mConfig[configMgr.mKey.CDKEY_LIST]:
            configMgr.mConfig[configMgr.mKey.CDKEY_LIST].append(cdkey)

        logMgr.Info(f"已添加兑换码:{cdkey}")
        return Response(f"已添加兑换码:{cdkey}")

    @mAppFlask.route('/cdkeylist/remove',methods=['POST'])
    def RemoveCdkeylist():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        cdkey = data['cdkey_list']
        if cdkey in configMgr.mConfig[configMgr.mKey.CDKEY_LIST]:
            if len(configMgr.mConfig[configMgr.mKey.CDKEY_LIST]) == 1:
                configMgr.mConfig.SetValue(configMgr.mKey.CDKEY_LIST, [])
            else:
                configMgr.mConfig[configMgr.mKey.CDKEY_LIST].remove(cdkey)

        logMgr.Info(f"已移除兑换码:{cdkey}")
        return Response(f"已移除兑换码:{cdkey}")

    @mAppFlask.route('/borrowchar/append',methods=['POST'])
    def AppendBorrowchar():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        char = data['borrow_character']
        if not char in configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER]:
            configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER].append(char)
            logMgr.Info(f"已添加助战角色:{dataMgr.meta['角色'][char]}")
            return Response(f"已添加助战角色:{dataMgr.meta['角色'][char]}")
        else:
            logMgr.Info(f"助战角色:{dataMgr.meta['角色'][char]}已重复!")
            return Response(f"助战角色:{dataMgr.meta['角色'][char]}已重复!")

    @mAppFlask.route('/borrowchar/remove',methods=['POST'])
    def RemoveBorrowchar():
        # configMgr.mConfigModule.ReloadConfig()
        data = request.get_json('data')
        char = data['borrow_character']
        if char in configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER]:
            if len(configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER]) == 1:
                configMgr.mConfig.SetValue(configMgr.mKey.BORROW_CHARACTER, [])
            else:
                configMgr.mConfig[configMgr.mKey.BORROW_CHARACTER].remove(char)

        logMgr.Info(f"已移除助战角色:{dataMgr.meta['角色'][char]}")
        return Response(f"已移除助战角色:{dataMgr.meta['角色'][char]}")
    
    @mAppFlask.route('/notify')
    def Notify():
        noticeList, annList = WebModule.GetNoticeAndAnn()
        return render_template('notify.html',configMgr=configMgr, url='notify',loginList=WebModule.InitLoginList(), noticeList=noticeList,annList=annList)

    @mAppFlask.route('/notify/all',methods=['POST'])
    def NotifyAll():

        data = request.get_json('data')
        notifyMgr.SendNotifyAll(f"全体公告:{data['notify_title']}", f"<p>{data['notify_content']}</p>", configMgr, dataMgr)
        logMgr.Info("全体公告已发送")
        return Response("全体公告已发送")

    @mAppFlask.route('/notify/single',methods=['POST'])
    def NotifySingle():

        data = request.get_json('data')
        notifyMgr.SendNotifySingle(f"单人通知:{data['notify_title']}", f"<p>{data['notify_content']}</p>", configMgr, dataMgr, data['notify_single'], configMgr.mConfig[configMgr.mKey.NOTIFY_SMTP_TO][data['notify_single']])
        logMgr.Info("单人通知已发送")
        return Response("单人通知已发送")