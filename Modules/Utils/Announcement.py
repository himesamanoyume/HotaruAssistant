import requests,json

class Announcement:
    def GetNotify():
        r = requests.get("https://ann.himesamanoyume.top/announcement.json")
        if r.status_code == 200:
            data = json.loads(r.text)
            announcement = data['announcement']
            
            print("\n--------------------公告--------------------\n")
            for item in announcement:
                print(f"【{item['Title']}】:{item['Content']}")
                print("\n--------------------------------------------\n")