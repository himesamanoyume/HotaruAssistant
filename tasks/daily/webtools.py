from module.config.config import Config
import time,requests,random,json
from datetime import datetime

config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
ts = open("./assets/config/task_score_mappings.json", 'r', encoding='utf-8')
task_score = json.load(ts)
ts.close()
rb = open("./assets/config/ruby_detail.json", 'r', encoding='utf-8')
ruby = json.load(rb)
rb.close()
version_txt = open("./assets/config/version.txt", "r", encoding='utf-8')
version = version_txt.read()
version_txt.close()
css = open("./assets/css/common.css", 'r', encoding='utf-8')
htmlStyle = css.read()
css.close()

class WebTools:
    def official_notice():
        r = requests.get("https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&channel_id=1&level=1&platform=pc&region=prod_gf_cn&uid=1")
        data = json.loads(r.text)
        data=data['data']['pic_list'][0]['type_list'][0]['list']
        datalist = list()
        for item in data:
            title = item['title']
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
    
    def official_content():
        r = requests.get("https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList?game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&bundle_id=hkrpg_cn&channel_id=1&level=1&platform=pc&region=prod_gf_cn&uid=1")
        data = json.loads(r.text)
        data=data['data']['pic_list'][0]['type_list'][0]['list']
        content = '<p>简易官方公告,进度条仅代表邮件发送时距离结束的进度!</p>'
        for item in data:
            title = item['title']
            start_time = item['start_time']
            end_time = item['end_time']
            start_time_stamp = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
            end_time_stamp = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
            progress = (time.time() - start_time_stamp) / (end_time_stamp - start_time_stamp)
            totalTime = end_time_stamp - time.time()
            _day = int(totalTime // 86400)
            _hour = int((totalTime - _day * 86400) // 3600)
            content += f"<div style='background-color:#40405f;margin:10px 0 0 0;'><p style='margin: 0 20px 0 20px;'>{title}</p><div style='font-size: 12px;line-height: 30px;padding: 0 20px;display: inline-block;transition-duration: .2s;'>{start_time} - {end_time}<br>{_day} 天 {_hour} 时后结束</div><div style='background-color: #66ccff;width:{progress * 100}%;max-width:100%;height:3px;'></div></div>"

        return content


    def config_content(multi_content, uid):
        config.reload()
        multi_content += f"<hr style=background:#d9d9d9><p><strong>配置详细</strong></p><div class=post-txt-container-datetime>该配置显示了当要挑战副本时会选择什么副本,如果配置与需求不符或需求有变化请和我说,然后我进行调整,否则我一律会首先遵照每个UID的配置来清体力</div>"
        multi_content += f"<p>清开拓力时将要打的副本类型:<span class=important style=background-color:#40405f;color:#66ccff>{config.instance_type[uid]}</span></p>"
        multi_content += f"<p>不同副本类型下的副本名称:</p>"

        with open("./assets/config/ruby_detail.json", 'r', encoding='utf-8') as ruby_json:
            ruby_mappings = json.load(ruby_json)

            nizaohuaejin_text = ''
            nizaohuaejin_text = ruby_mappings['拟造花萼（金）'][config.instance_names[uid]['拟造花萼（金）']]

            ningzhixuying_text = ''
            ningzhixuying_text = ruby_mappings['凝滞虚影'][config.instance_names[uid]['凝滞虚影']]

            qinshisuidong_text = ''
            qinshisuidong_text = ruby_mappings['侵蚀隧洞'][config.instance_names[uid]['侵蚀隧洞']]

            lizhanyuxiang_text = ''
            lizhanyuxiang_text = ruby_mappings['历战余响'][config.instance_names[uid]['历战余响']]

            multi_content += f"<p>拟造花萼（金）:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['拟造花萼（金）']}<rt class='ttt' style='background-color: unset;' data-rt='{nizaohuaejin_text}'></rt></ruby></span></p>"
            multi_content += f"<p>拟造花萼（赤）:<span class=important style=background-color:#40405f;color:#66ccff>{config.instance_names[uid]['拟造花萼（赤）']}</span></p>"
            multi_content += f"<p>凝滞虚影:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['凝滞虚影']}<rt class='ttt' style='background-color: unset;' data-rt='{ningzhixuying_text}'></rt></ruby></span></p>"
            multi_content += f"<p>侵蚀隧洞:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['侵蚀隧洞']}<rt class='ttt' style='background-color: unset;' data-rt='{qinshisuidong_text}'></rt></ruby></span></p>"
            multi_content += f"<p>是否清空3次历战余响:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if config.echo_of_war_enable[uid] else '否'}</span></p>"
            multi_content += f"<p>历战余响:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{config.instance_names[uid]['历战余响']}<rt class='ttt' style='background-color: unset;' data-rt='{lizhanyuxiang_text}'></rt></ruby></span></p>"
            multi_content += f"<p>是否允许我分解4星及以下遗器:<span class=important style=background-color:#40405f;color:#66ccff>{'是' if config.relic_salvage_enable[uid] else '否'}</span></p>"

            if config.universe_number[uid] in [3,4,5,6,7,8]:
                world_number = ruby_mappings['模拟宇宙'][str(config.universe_number[uid])]
                world_relic = ruby_mappings['模拟宇宙遗器'][str(config.universe_number[uid])]
            else:
                world_number = '世界选择有误'
                world_relic = ''

            universe_content = ''
            universe_content += f"<p>模拟宇宙:<span class=important style=background-color:#40405f;color:#66ccff><ruby>{world_number}<rt class='ttt' style='background-color: unset;' data-rt='{world_relic}'></rt></ruby></span></p>"

            return multi_content, universe_content

    def aside_content():
        aside_content = f"""
        <aside class=info-container>
                            <div class=info-container-inner id=info-container-inner style='margin-top:10px'>
                                <div class=info style=background-color:#2b2b2b>
                                    <div class=fiximg style=width:100%;border-bottom-left-radius:0;border-bottom-right-radius:0;display:block>
                                        <div class=fiximg__container style=display:block;margin:0>
                                            <img class=info-icon loading=lazy src=https://blog.himesamanoyume.top/usericon.webp style=margin-top:20px;max-height:185px;border-radius:3px;max-width:185px;width:100%;border:0;background-color:#66ccff>
                                        </div>
                                    </div>
                                    <div class=info-name style=color:#d9d9d9>
                                        <ruby>姫様の夢<rt class='ttt' data-rt='Ginka可爱捏'></rt></ruby>
                                    </div>
                                    <div class=info-txt style=color:#d9d9d9>
                                        Princess Dreamland
                                    </div>
                                </div>
                            </div>
                        </aside>
                    </div>
                </main>
                <footer class=footer style=color:#d9d9d9>
                    <div class=footer-content>
                        Copyright © 2021-2024 @姫様の夢
                    </div>
                    <div class=footer-content>
                        <a>HIMEPRODUCER</a> {version}
                    </div>
                </footer>
            </div>
        """
        return aside_content

    def head_content(contentTitle):
        randomNumber = random.randint(0,4)
        head_content = f"""
        <div class=body style=background-color:#3a3a3a>
            <style>{htmlStyle}</style>
                <header class=header style=position:sticky>
                    <nav class=nav style='margin:0 15px;justify-content:center;background-color:#2b2b2b'>
                        <span class=blogName style=color:#d9d9d9 id=nav-index>
                            HIMEPRODUCER
                        </span>
                    </nav>
                </header>
                <main class=main>
                    <div class=home-container>
                        <div class=post-container style=margin:0;box-sizing:border-box;max-width:100%;width:100%;height:100%;border:0>
                            <div class=post style=background-color:#2b2b2b>
                                <div class=post-Img-container>
                                    <img id=_index loading=lazy src=https://blog.himesamanoyume.top/_index{randomNumber}.webp data-zoomable/>
                                </div>
                                <div class=post-txt-container>
                                    <div class=post-txt-container-title style=color:#d9d9d9>
                                        <h4 style=color:#66ccff>
                                            {contentTitle}
                                        </h4>
                                    </div>
                        """
        return head_content
