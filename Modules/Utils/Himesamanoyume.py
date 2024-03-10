import requests,json,base64
from Hotaru.Server.LogServerHotaru import logMgr

class Himesamanoyume:
    def PrincessDreamland():
        cnJy = requests.get("{Y2FvbmltYWRl}{ZGFvbWFpZ291}".format(ZGFvbWFpZ291=base64.b64decode("L0hvdGFydUFzc2lzdGFudC9tYWluL2Fzc2V0cy9jb25maWcvbWV0YS5qc29u").decode('utf-8'),Y2FvbmltYWRl=base64.b64decode("aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2hpbWVzYW1hbm95dW1l").decode('utf-8')))
        if cnJy.status_code == 200:
            ZGF0YWFh=json.loads(cnJy.text)
            YW5ub3VuY2VtZW50=ZGF0YWFh["{YW5ub3VuY2VtZW50}".format(YW5ub3VuY2VtZW50=base64.b64decode("YW5ub3VuY2VtZW50").decode('utf-8'))]
            logMgr.Hr(base64.b64decode("B|5YWs5ZGK".split('|')[1]).decode('utf-8'), 2)
            for aWl0ZW1t in YW5ub3VuY2VtZW50:
                logMgr.Hr(f"【{aWl0ZW1t['Title']}】:{aWl0ZW1t['Content']}")