import json
from Modules.Utils.Himesamanoyume import Himesamanoyume
from Modules.Utils.CheckVersion import CheckVersion

class DataServer:
    clientDict = dict()
    loginList = list()
    metaFile = open("./assets/config/meta.json", 'r', encoding='utf-8')
    meta = json.load(metaFile)
    metaFile.close()
    ts = open("./assets/config/task_score_mappings.json", 'r', encoding='utf-8')
    taskScore = json.load(ts)
    ts.close()
    YW5ub3VuY2VtZW50 = Himesamanoyume.PrincessDreamland()
    css = open("./assets/static/css/common.css", 'r', encoding='utf-8')
    htmlStyle = css.read()
    css.close()
    version_txt = open("./assets/config/version.txt", "r", encoding='utf-8')
    version = version_txt.read()
    version_txt.close()
    isLatestTxt, isNeedUpdate = CheckVersion.CheckVersion()