import requests,json,base64

class Himesamanoyume:
    def PrincessDreamland():
        cnJy = requests.get("{Y2FvbmltYWRl}{ZGFvbWFpZ291}".format(ZGFvbWFpZ291=base64.b64decode("dGh1YnVzZXJjb250ZW50LmNvbS9oaW1lc2FtYW5veXVtZS9Ib3RhcnVBc3Npc3RhbnQvbWFpbi9hc3NldHMvY29uZmlnL21ldGEuanNvbg==").decode('utf-8'),Y2FvbmltYWRl=base64.b64decode("aHR0cHM6Ly9naXRodWIubW9leXkueHl6L2h0dHBzOi8vcmF3Lmdp").decode('utf-8')))
        if cnJy.status_code == 200:
            ZGF0YWFh=json.loads(cnJy.text)
            YW5ub3VuY2VtZW50=ZGF0YWFh["{YW5ub3VuY2VtZW50}".format(YW5ub3VuY2VtZW50=base64.b64decode("YW5ub3VuY2VtZW50").decode('utf-8'))]
            return YW5ub3VuY2VtZW50
        else:
            print(cnJy.text)
            return False