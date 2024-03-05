
from . import *
from Hotaru.Client.LogClientHotaru import logClientMgr
from .BaseConfigModule import BaseConfigModule
from .ConfigKeySubModule import ConfigKeySubModule

class ConfigClientModule(BaseConfigModule):

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance

    @classmethod
    def IsAgreeDisclaimer(cls):
        if not cls.GetConfigValue(ConfigKeySubModule.AGREED_TO_DISCLAIMER, None):
            logClientMgr.Error("你未同意《免责声明》, 需要先启动Server并同意")
            input("按回车键关闭窗口. . .")
            sys.exit(0)


    @classmethod
    def GetConfigValue(cls, key, uid=None):
        url = 'http://127.0.0.1:5000/api/getConfigValue'
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length':'<calculated when request is sent>'
        }
        data = {'key': key, 'uid': uid }
        result = requests.post(url, headers=header, data=data)
        data = json.loads(result.text)
        return data['value']

    
    @classmethod
    def SetConfigValue(cls, key, uid = None, value=0):
        url = 'http://127.0.0.1:5000/api/setConfigValue'
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length':'<calculated when request is sent>'
        }
        data = {'key': key, 'uid': uid , 'value': value}
        requests.post(url, headers=header, data=data)

    @classmethod
    def DelConfigKey(cls, key, uid = None, value=0):
        url = 'http://127.0.0.1:5000/api/delConfigKey'
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length':'<calculated when request is sent>'
        }
        data = {'key': key, 'uid': uid , 'value': value}
        requests.post(url, headers=header, data=data)

    @classmethod
    def AppendConfigValue(cls, key, uid = None, value=0):
        url = 'http://127.0.0.1:5000/api/appendConfigValue'
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length':'<calculated when request is sent>'
        }
        data = {'key': key, 'uid': uid , 'value': value}
        requests.post(url, headers=header, data=data)
        
