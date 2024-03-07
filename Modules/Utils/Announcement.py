import requests,json
from Hotaru.Server.LogServerHotaru import logMgr

class Announcement:
    def GetNotify():
        r = requests.get("https://ann.himesamanoyume.top/announcement.json")
        if r.status_code == 200:
            data = json.loads(r.text)
            announcement = data['announcement']
            
            logMgr.Hr("公告", 2)
            for item in announcement:
                logMgr.Hr(f"【{item['Title']}】:{item['Content']}")