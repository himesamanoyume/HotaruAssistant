import requests,json,base64

class Himesamanoyume:
    def PrincessDreamland():
        url1 = "{Y2FvbmltYWRl}{ZGFvbWFpZ291}".format(ZGFvbWFpZ291=base64.b64decode("dGh1YnVzZXJjb250ZW50LmNvbS9oaW1lc2FtYW5veXVtZS9Ib3RhcnVBc3Npc3RhbnQvbWFpbi9hc3NldHMvY29uZmlnL21ldGEuanNvbg==").decode('utf-8'),Y2FvbmltYWRl=base64.b64decode("aHR0cHM6Ly9naXRodWIuaGltZXNhbWFub3l1bWUudG9wL2h0dHBzOi8vcmF3Lmdp").decode('utf-8'))

        url2 = "{Y2FvbmltYWRl}{ZGFvbWFpZ291}".format(ZGFvbWFpZ291=base64.b64decode("dGh1YnVzZXJjb250ZW50LmNvbS9oaW1lc2FtYW5veXVtZS9Ib3RhcnVBc3Npc3RhbnQvbWFpbi9hc3NldHMvY29uZmlnL21ldGEuanNvbg==").decode('utf-8'),Y2FvbmltYWRl=base64.b64decode("aHR0cHM6Ly9naXRodWIuaGltZXNhbWFub3l1bWUudG9wL2h0dHBzOi8vcmF3Lmdp").decode('utf-8'))

        cnJy = requests.get(url1)
        if cnJy.status_code == 200:
            ZGF0YWFh=json.loads(cnJy.text)
            YW5ub3VuY2VtZW50=ZGF0YWFh["{YW5ub3VuY2VtZW50}".format(YW5ub3VuY2VtZW50=base64.b64decode("YW5ub3VuY2VtZW50").decode('utf-8'))]
            return YW5ub3VuY2VtZW50
        else:
            cnJy2 = requests.get(url2)
            if cnJy2.status_code == 200:
                ZGF0YWFh=json.loads(cnJy.text)
                YW5ub3VuY2VtZW50=ZGF0YWFh["{YW5ub3VuY2VtZW50}".format(YW5ub3VuY2VtZW50=base64.b64decode("YW5ub3VuY2VtZW50").decode('utf-8'))]
                return YW5ub3VuY2VtZW50
            else:
                print(cnJy.text)
                print(cnJy2.text)
                return False