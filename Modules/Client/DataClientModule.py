from Modules.Utils.Himesamanoyume import Himesamanoyume
import json,base64

class DataClientModule:
    tempUid = '-1'
    currentUid = '-1'
    currentGamePid = -1 # 初始值 不要动
    currentPower = 2400
    currentImmersifiers = 0
    currentRelicsCount = 0
    currentHimekoTimes = 0
    loginDict = dict()
    loginList = list()
    loopStartTimestamp = 0
    currentAction = "临时流程"
    currentState = 'TempState'
    currentDailyTasksScore = 0
    dailyTasksHasBeenChecked = False
    tempDailyTasksList = {}
    dailyTasksFunctions = {}
    currentUniverseScore = 0
    maxCurrentUniverseScore = 1
    YW5ub3VuY2VtZW50 = [{"Title":"{Y2NvbnRlbnR0}".format(Y2NvbnRlbnR0=base64.b64decode("5pyq6IO96I635Y+W5Yiw5YWs5ZGK").decode('utf-8')),"Content":"{Y2NvbnRlbnR0}".format(Y2NvbnRlbnR0=base64.b64decode("5pyq6IO96I635Y+W5Yiw5YWs5ZGK").decode('utf-8'))}]
    gameTitleName = ''
    tempText = ''
    passRemaining = ''
    css = open("./assets/static/css/common.css", 'r', encoding='utf-8')
    htmlStyle = css.read()
    css.close()
    versionTxt = open("./assets/config/version.txt", "r", encoding='utf-8')
    version = versionTxt.read()
    versionTxt.close()
    metaFile = open("./assets/config/meta.json", 'r', encoding='utf-8')
    meta = json.load(metaFile)
    metaFile.close()
    notifyContent = {
        "上号时长": "",
        "开拓力回满时间": "",
        "遗器数量": 0,
        "副本情况":{
            "历战余响":0,
            "侵蚀隧洞":0,
            "凝滞虚影":0,
            "拟造花萼（金）":0,
            "拟造花萼（赤）":0,
            "饰品提取":0,
            "差分宇宙":0
        },
        "混沌回忆1层数": -1,
        "混沌回忆1星数": -1,
        "混沌回忆1倒计时": "",
        "混沌回忆2层数": -1,
        "混沌回忆2星数": -1,
        "混沌回忆2倒计时": "",
        "虚构叙事1层数": -1,
        "虚构叙事1星数": -1,
        "虚构叙事1倒计时": "",
        "虚构叙事2层数": -1,
        "虚构叙事2星数": -1,
        "虚构叙事2倒计时": "",
        "末日幻影1层数": -1,
        "末日幻影1星数": -1,
        "末日幻影1倒计时": "",
        "末日幻影2层数": -1,
        "末日幻影2星数": -1,
        "末日幻影2倒计时": "",
        "遗器胚子": []
    }

    def PrincessDreamland(self):
        self.YW5ub3VuY2VtZW50 = Himesamanoyume.PrincessDreamland()

    def ResetData(self):
        self.tempUid = '-1'
        self.currentUid = '-1'
        self.currentGamePid = -1
        self.loopStartTimestamp = 0
        self.currentAction = "临时流程"
        self.currentState = 'TempState'
        self.currentPower = 2400
        self.currentImmersifiers = 0
        self.currentRelicsCount = 0
        self.currentHimekoTimes = 0
        self.tempDailyTasksList = {}
        self.dailyTasksHasBeenChecked = False
        self.currentDailyTasksScore = 0
        self.dailyTasksFunctions = {}
        self.currentUniverseScore = 0
        self.maxCurrentUniverseScore = 1
        self.tempText = ''
        self.passRemaining = ''
        self.notifyContent = {
            "上号时长": "",
            "开拓力回满时间": "",
            "遗器数量": 0,
            "副本情况":{
                "历战余响":0,
                "侵蚀隧洞":0,
                "凝滞虚影":0,
                "拟造花萼（金）":0,
                "拟造花萼（赤）":0,
                "饰品提取":0,
                "差分宇宙":0
            },
            "混沌回忆1层数": -1,
            "混沌回忆1星数": -1,
            "混沌回忆1倒计时": "",
            "混沌回忆2层数": -1,
            "混沌回忆2星数": -1,
            "混沌回忆2倒计时": "",
            "虚构叙事1层数": -1,
            "虚构叙事1星数": -1,
            "虚构叙事1倒计时": "",
            "虚构叙事2层数": -1,
            "虚构叙事2星数": -1,
            "虚构叙事2倒计时": "",
            "末日幻影1层数": -1,
            "末日幻影1星数": -1,
            "末日幻影1倒计时": "",
            "末日幻影2层数": -1,
            "末日幻影2星数": -1,
            "末日幻影2倒计时": "",
            "遗器胚子": []
        }
