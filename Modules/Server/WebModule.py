from flask import Flask,render_template,request,abort,Response
from Hotaru.Server.ConfigServerHotaru import configServerMgr
import json


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
        return render_template('test.html')
    
    # @mAppFlask.route('/api/getConfigValue', methods=['POST'])
    # def GetConfigValue():
    #     key = request.form.get('key')
    #     uid = request.form.get('uid')
    #     value = configServerMgr.GetConfigValue(key, uid)
    #     print(f"{key}获取一个值:{value}")
    #     data1 = {'value': value}
    #     data2 = json.dumps(data1)
    #     return Response(data2)
    
    # @mAppFlask.route('/api/setConfigValue', methods=['POST'])
    # def SetConfigValue():
    #     key = request.form.get('key')
    #     uid = request.form.get('uid')
    #     value = request.form.get('value')
    #     configServerMgr.SetConfigValue(key, uid, value)
    #     return Response()
    
    # @mAppFlask.route('/api/appendConfigValue', methods=['POST'])
    # def AppendConfigValue():
    #     key = request.form.get('key')
    #     uid = request.form.get('uid')
    #     value = request.form.get('value')
    #     configServerMgr.AppendConfigValue(key, uid, value)
    #     return Response()
    
    # @mAppFlask.route('/api/delConfigKey', methods=['POST'])
    # def DelConfigKey():
    #     key = request.form.get('key')
    #     uid = request.form.get('uid')
    #     value = request.form.get('value')
    #     configServerMgr.DelConfigKey(key, uid, value)
    #     return Response()
            