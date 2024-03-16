from Modules.Utils.Himesamanoyume import Himesamanoyume

class DataClient:
    tempUid = -1
    currentUid = -1
    currentGamePid = -1 # 初始值 不要动
    currentPower = 2400
    currentImmersifiers = 0
    currentRelicCount = 0
    currentHimekoTimes = 0
    loginDict = dict()
    loginList = list()
    loopStartTimestamp = 0
    currentAction = "临时流程"
    css = open("./assets/static/css/common.css", 'r', encoding='utf-8')
    htmlStyle = css.read()
    css.close()
    version_txt = open("./assets/config/version.txt", "r", encoding='utf-8')
    version = version_txt.read()
    version_txt.close()
    YW5ub3VuY2VtZW50 = Himesamanoyume.PrincessDreamland()

    def ResetData(self):
        self.currentUid = -1
        self.currentGamePid = -1
        self.loopStartTimestamp = 0
        self.currentAction = "临时流程"
        self.currentPower = 2400
        self.currentImmersifiers = 0
        self.currentRelicCount = 0
        self.currentHimekoTimes = 0
