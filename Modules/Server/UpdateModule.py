from Hotaru.Server.LogServerHotaru import logServerMgr
from Hotaru.Server.ConfigServerHotaru import configServerMgr
from Modules.Utils.FastestMirror import FastestMirror
import requests,json
from packaging.version import parse

class UpdateModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def DetectUpdate():
        if not configServerMgr.GetConfigValue(configServerMgr.mConfig.mCommonKey.check_update):
            logServerMgr.Error("检测更新未开启")
            return False
        logServerMgr.Info("开始检测更新")
        try:
            response = requests.get(FastestMirror.GetGithubApiMirror("himesamanoyume","HotaruAssistant","latest.json",1), timeout=3)
            if response.status_code == 200:
                data = json.loads(response.text)
                version:str = data["tag_name"]
                logServerMgr.Info(f"最新版本:{version},当前版本:{configServerMgr.GetConfigValue(configServerMgr.mConfig.mCommonKey.hotaru_version)}")
                if parse(version.lstrip('v')) > parse(configServerMgr.mConfig.mCommonKey.hotaru_version.lstrip('v')):
                    logServerMgr.Info(f"发现新版本,请退出程序使用Update.exe进行更新")
                    logServerMgr.Info(data["html_url"])
                else:
                    logServerMgr.Info("已经是最新版本")
            else:
                logServerMgr.Error("检测更新失败")
                # logger.debug(response.text)
        except Exception as e:
            logServerMgr.Error("检测更新失败")
            # logger.debug(e)
        logServerMgr.Info("完成")