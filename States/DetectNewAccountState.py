from States import *
from Hotaru.Client.ConfigClientHotaru import configClientMgr
from Modules.Utils.Data import Data
from Modules.Utils.Date import Date

class DetectNewAccountState(BaseState):
    mStateName = 'DetectNewAccountState'

    def OnBegin(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Begin"))
        return False

    def OnRunning(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Running"))
        log.info(logClientMgr.Info("正在检测是否有新注册表加入"))
        wantRegisterAccounts = configClientMgr.mConfig[configClientMgr.mKey.WANT_REGISTER_ACCOUNTS]
        if len(wantRegisterAccounts) > 1:
            log.warning(logClientMgr.Warning("检测到有新注册表加入"))
            for uid, item in wantRegisterAccounts.items():
                if uid == '111111111': continue
                if item['reg_path']=='':
                    log.error(logClientMgr.Error(f"{uid}:新的注册信息中注册表地址未完整填写"))
                    input("按下回车跳过该次注册")
                    return
                if item['email']=='':
                    log.error(logClientMgr.Error(f"{uid}:新的注册信息中邮箱未完整填写"))
                    input("按下回车跳过该次注册")
                    return
                if not len(item['universe_team']) == 4:
                    log.error(logClientMgr.Error(f"{uid}:新的注册信息中模拟宇宙小队角色未填写满4人或超出4人"))
                    input("按下回车跳过该次注册")
                    return
                if not item['universe_fate'] in [0,1,2,3,4,5,6,7,8]:
                    log.error(logClientMgr.Error(f"{uid}:新的注册信息中模拟宇宙命途不合法"))
                    input("按下回车跳过该次注册")
                    return
                if not item['universe_number'] in [3,4,5,6,7,8]:
                    log.error(logClientMgr.Error(f"{uid}:新的注册信息中模拟宇宙选择的世界不合法"))
                    input("按下回车跳过该次注册")
                    return
                if not item['universe_difficulty'] in [1,2,3,4,5]:
                    log.error(logClientMgr.Error(f"{uid}:新的注册信息中模拟宇宙难度不合法"))
                    input("按下回车跳过该次注册")
                    return

                multiLoginAccounts = configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS]
                if multiLoginAccounts == {}:
                    tempList = list()
                    tempList.append(item['reg_path'])
                    configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS] = tempList
                else:
                    configClientMgr.mConfig[configClientMgr.mKey.MULTI_LOGIN_ACCOUNTS].append(item['reg_path'])

                Data.loginList.append(f"{str(item['reg_path'])}")
                configClientMgr.mConfig[configClientMgr.mKey.NOTIFY_SMTP_TO][uid] = item['email']
                configClientMgr.mConfig[configClientMgr.mKey.UNIVERSE_DIFFICULTY][uid] = item['universe_number']
                configClientMgr.mConfig[configClientMgr.mKey.UNIVERSE_NUMBER][uid] = item['universe_difficulty']
                configClientMgr.mConfig[configClientMgr.mKey.UNIVERSE_FATE][uid] = item['universe_fate']
                configClientMgr.mConfig[configClientMgr.mKey.UNIVERSE_TEAM][uid] = item['universe_team']
        return False

    def OnExit(self):
        # log.info(logClientMgr.Info(f"{self.mStateName} Exit"))
        return False