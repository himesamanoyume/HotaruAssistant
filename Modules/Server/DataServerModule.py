import json
from Modules.Utils.Himesamanoyume import Himesamanoyume

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