from Modules.Utils.Himesamanoyume import Himesamanoyume
import json

class DataClient:
    tempUid = '-1'
    currentUid = '-1'
    currentGamePid = -1 # 初始值 不要动
    currentPower = 2400
    currentImmersifiers = 0
    currentRelicCount = 0
    currentHimekoTimes = 0
    loginDict = dict()
    loginList = list()
    loopStartTimestamp = 0
    currentAction = "临时流程"
    currentDailyTasksScore = 0
    dailyTasksHasBeenChecked = False
    tempDailyTasksList = {}
    dailyTasksFunctions = {}
    currentUniverseScore = 0
    maxCurrentUniverseScore = 1
    isDetectUniverseScoreAndFinished = False
    gameTitleName = ''
    css = open("./assets/static/css/common.css", 'r', encoding='utf-8')
    htmlStyle = css.read()
    css.close()
    version_txt = open("./assets/config/version.txt", "r", encoding='utf-8')
    version = version_txt.read()
    version_txt.close()
    metaFile = open("./assets/config/meta.json", 'r', encoding='utf-8')
    meta = json.load(metaFile)
    metaFile.close()
    YW5ub3VuY2VtZW50 = Himesamanoyume.PrincessDreamland()
    notifyContent = {
        "上号时长": "",
        "下线时开拓力": 0,
        "开拓力回满时间": "",
        "遗器数量": 0,
        "副本情况":{
            "历战余响":0,
            "侵蚀隧洞":0,
            "凝滞虚影":0,
            "拟造花萼（金）":0,
            "拟造花萼（赤）":0,
            "模拟宇宙":0
        },
        "混沌回忆倒计时": "",
        "虚构叙事倒计时": "",
        "遗器胚子": []
    }

    def ResetData(self):
        self.tempUid = '-1'
        self.currentUid = '-1'
        self.currentGamePid = -1
        self.loopStartTimestamp = 0
        self.currentAction = "临时流程"
        self.currentPower = 2400
        self.currentImmersifiers = 0
        self.currentRelicCount = 0
        self.currentHimekoTimes = 0
        self.tempDailyTasksList = {}
        self.dailyTasksHasBeenChecked = False
        self.currentDailyTasksScore = 0
        self.dailyTasksFunctions = {}
        self.currentUniverseScore = 0
        self.maxCurrentUniverseScore = 1
        self.notifyContent = {
            "上号时长": "",
            "下线时开拓力": 0,
            "开拓力回满时间": "",
            "遗器数量": 0,
            "副本情况":{
                "历战余响":0,
                "侵蚀隧洞":0,
                "凝滞虚影":0,
                "拟造花萼（金）":0,
                "拟造花萼（赤）":0,
                "模拟宇宙":0
            },
            "混沌回忆倒计时": "",
            "虚构叙事倒计时": "",
            "遗器胚子":[]
        }
