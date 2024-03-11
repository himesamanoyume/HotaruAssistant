import requests,time,json

class NotifyModule:
    
    def __init__(self):
        pass
    
    @staticmethod
    def CreateOfficialNotice():
        r = requests.get("https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&channel_id=1&level=1&platform=pc&region=prod_gf_cn&uid=1")
        if r.status_code == 200:
            data = json.loads(r.text)
            data=data['data']['pic_list'][0]['type_list'][0]['list']
            datalist = list()
            for item in data:
                title = item['title']
                if title == '':
                    continue
                start_time = item['start_time']
                end_time = item['end_time']
                start_time_stamp = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
                end_time_stamp = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
                progress = (time.time() - start_time_stamp) / (end_time_stamp - start_time_stamp)
                totalTime = end_time_stamp - time.time()
                _day = int(totalTime // 86400)
                _hour = int((totalTime - _day * 86400) // 3600)
                datalist.append({"title":title,"start_time":start_time,"end_time":end_time,"progress": progress, "day":_day,"hour":_hour})

            return datalist
        else:
            return False

        