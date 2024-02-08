from managers.logger_manager import logger
from managers.config_manager import config
from managers.screen_manager import screen
from managers.automation_manager import auto
import time
from datetime import datetime
from managers.translate_manager import _
from managers.utils_manager import gu
from tasks.base.date import Date
from tasks.daily.photo import Photo
from managers.notify_manager import notify
from tasks.daily.fight import Fight
from tasks.weekly.universe import Universe
from tasks.reward.reward import Reward
from tasks.daily.synthesis import Synthesis
from tasks.daily.relics import Relics
from tasks.daily.utils import Utils
from tasks.weekly.forgottenhall import ForgottenHall
from tasks.weekly.purefiction import PureFiction
from tasks.weekly.echoofwar import Echoofwar
from tasks.power.power import Power
from tasks.daily.tasks import Tasks
from tasks.activity.activity import Activity
from tasks.daily.himekotry import HimekoTry
import pyperclip

class Daily:
    def sub():
        config.reload()
        logger.info(gu("进入历战余响部分"))
        if config.echo_of_war_enable[Utils.get_uid()]:
            if Echoofwar.echoofwar_get_times() > 0:
                Echoofwar.start()
            else:
                if Utils.is_next_mon_4_am(config.echo_of_war_timestamp, Utils.get_uid()):
                    config.save_config()
                else:
                    logger.info(gu("历战余响尚\033[91m未刷新\033[0m"))
        else:
            logger.info(gu("历战余响\033[91m未开启\033[0m"))

        logger.info(gu("进入清体力部分"))
        Power.start()
        
        logger.info(gu("进入模拟宇宙部分"))
        Universe.open_universe_score_screen()
        Universe.get_immersifier()

    def start_ready():
        if config.recording_enable:
            auto.press_key(config.hotkey_obs_start)
        
        config.reload()
        Utils.get_new_uid()
        Utils._content.update({'uid':Utils.get_uid()})
        Utils.getDailyScoreMappings()
        Tasks._isDetect = False

        if Utils.is_next_4_am(config.last_run_timestamp, Utils.get_uid()):
            config.save_config()
            logger.info(gu("已是新的一天,开始每日"))
            # 活动
            Activity.start()

            screen.change_to("guide2")

            tasks = Tasks("./assets/config/task_mappings.json")
            tasks.start(Utils.get_uid())
            Reward.start()

            config.set_value("daily_tasks", tasks.daily_tasks)
            Utils.saveTimestamp('last_run_timestamp', Utils.get_uid())

        else:
            logger.info(gu("日常任务\033[91m未刷新\033[0m"))

    @staticmethod
    def start():
        config.reload()
        if config.multi_login:
            logger.hr(gu("多账号下开始日常任务"), 0)

        Daily.start_ready()

        Utils.calcDailyTasksScore(Utils.get_uid())

        Power.power()

        if len(config.daily_tasks[Utils.get_uid()]) > 0:
            task_functions = {
                "拍照1次": lambda: Photo.photograph(),
                "合成1次消耗品": lambda: Synthesis.consumables(),
                "合成1次材料": lambda: Synthesis.material(),
                "使用1次「万能合成机」": lambda: Synthesis.material(),
                "使用1件消耗品": lambda: Synthesis.use_consumables(),
                "完成1次「拟造花萼（金）」": lambda: Power.instance("拟造花萼（金）", config.instance_names[Utils.get_uid()]["拟造花萼（金）"], 10, 1),
                "完成1次「拟造花萼（赤）」": lambda: Power.instance("拟造花萼（赤）", config.instance_names[Utils.get_uid()]["拟造花萼（赤）"], 10, 1),
                "完成1次「凝滞虚影」": lambda: Power.instance("凝滞虚影", config.instance_names[Utils.get_uid()]["凝滞虚影"], 30, 1),
                "完成1次「侵蚀隧洞」": lambda: Power.instance("侵蚀隧洞", config.instance_names[Utils.get_uid()]["侵蚀隧洞"], 40, 1),
                "完成1次「历战余响」": lambda: Power.instance("历战余响", config.instance_names[Utils.get_uid()]["历战余响"], 30, 1),
                "累计施放2次秘技": lambda: HimekoTry.technique(),
                "累计击碎3个可破坏物": lambda: HimekoTry.item(),
                "单场战斗中，触发3种不同属性的弱点击破": lambda: HimekoTry.weakness_diffrent_3(),
                "累计触发弱点击破效果5次": lambda: HimekoTry.weakness_5(),
                "累计消灭20个敌人": lambda: HimekoTry.enemy_20(),
                "利用弱点进入战斗并获胜3次": lambda: HimekoTry.weakness_to_fight(),
                "施放终结技造成制胜一击1次": lambda: HimekoTry.final_skill_end(),
                # "通关「模拟宇宙」（任意世界）的1个区域": lambda: Universe.start(get_reward=False, nums=1, save=False),
                "分解任意1件遗器": lambda: Relics.salvage()
            }

            logger.hr(gu("今日实训"), 2)

            count = 0
            for key, value in config.daily_tasks[Utils.get_uid()].items():
                state = "\033[91m" + _("待完成") + "\033[0m" if value else "\033[92m" + _("已完成") + "\033[0m"
                logger.info(gu(f"{key}: {state}"))
                count = count + 1 if not value else count
            logger.info(gu(f"已完成:\033[93m{count}/{len(config.daily_tasks[Utils.get_uid()])}\033[0m"))

            # blacklist = {"单场战斗中，触发3种不同属性的弱点击破","累计触发弱点击破效果5次","利用弱点进入战斗并获胜3次","施放终结技造成制胜一击1次"}

            for task_name, task_value in config.daily_tasks[Utils.get_uid()].items():
                if f"{task_name}" in task_functions.keys():
                    if config.daily_tasks[Utils.get_uid()][task_name]:
                        if config.daily_tasks_fin[Utils.get_uid()]:
                            logger.info(gu(f"因每日任务已完成,【{task_name}】\033[92m跳过\033[0m"))
                            continue
                        if task_functions[f"{task_name}"]():
                            # if task_name in blacklist:
                            #     continue
                            logger.info(gu(f"{task_name}已完成"))
                            config.daily_tasks[Utils.get_uid()][task_name] = False
                            Utils.showDailyTasksScore(task_name, Utils.get_uid())                     
                            # config.save_config()
                        else:
                            if not config.daily_tasks_fin[Utils.get_uid()]:
                                logger.warning(gu(f"【{task_name}】可能对应选项\033[91m未开启\033[0m,请自行解决"))
                    else:
                        logger.info(gu(f"【{task_name}】该任务\033[92m已完成\033[0m,跳过"))
                else:
                    logger.warning(gu(f"【{task_name}】可能该任务\033[91m暂不支持\033[0m,跳过"))                                              
            
            Reward.start()
            logger.hr(gu("每日部分结束"), 2)

            count = 0
            for key, value in config.daily_tasks[Utils.get_uid()].items():
                count = count + 1 if not value else count

            logger.info(gu(f"已完成:\033[93m{count}/{len(config.daily_tasks[Utils.get_uid()])}\033[0m"))
            Utils.calcDailyTasksScore(Utils.get_uid())
            
        logger.hr(gu("完成"), 2)
        Daily.sub()
        Daily.end()
    
    def end():
        config.reload()
        Power.power()
        ForgottenHall.get_star_and_level()
        PureFiction.get_star_and_level()
        screen.change_to('menu')
        Reward.start()
        if len(config.cdkey_list) > 0:
            Daily.get_cdkey()
        Relics.detect_relic_count()
        Echoofwar.echoofwar_get_times()
        Utils.calcDailyTasksScore(Utils.get_uid())
        auto.press_key(config.hotkey_obs_stop)
        totalTime = time.time() - Utils._start_timestamp
        Utils._totalTime = totalTime
        if totalTime >= 3600:
            logger.warning(gu(f"{Utils.get_uid()}运行时长超时警告!"))
            notify.announcement(f"{Utils.get_uid()}运行时长超时警告!","该UID运行总时长超60分钟,不健康,请立即检查优化", isSingle=True)
            
        _day = int(totalTime // 86400)
        _hour = int((totalTime - _day * 86400) // 3600)
        _minute = int(((totalTime - _day *86400) - _hour * 3600) // 60)
        _second = int(((totalTime - _day *86400) - _hour * 3600) - _minute * 60)
        Utils._content['running_time'] = (f"{_day}天" if not _day == 0 else '') + (f"{_hour}小时" if not _hour == 0 else '') + (f"{_minute}分" if not _minute == 0 else '') + f"{_second}秒"
        logger.info(gu(f"本次运行时长:{Utils._content['running_time']}"))

    def get_cdkey():
        screen.change_to("cdkey")
        config.reload()
        for cdkey in config.cdkey_list:
            logger.info(gu("检测到有兑换码"))
            time.sleep(1)
            pyperclip.copy(cdkey)
            if auto.click_element("./assets/images/screen/cdkey/cdkey_copy.png", "image", 0.9, max_retries=5):
                time.sleep(0.5)
                if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=5):
                    time.sleep(0.5)
                    if auto.find_element("./assets/images/screen/cdkey/cdkey_fast.png", "image", 0.9, max_retries=5):
                        logger.warning(gu(f"{cdkey},兑换过快,5秒后重试"))
                        time.sleep(5)
                        if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=5):
                            time.sleep(0.5)
                            if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=5):
                                logger.info(gu(f"{cdkey},兑换成功"))
                                time.sleep(1)
                                screen.change_to("cdkey")
                                continue
                    elif auto.find_element("./assets/images/screen/cdkey/cdkey_repeat.png", "image", 0.9, max_retries=5):
                        logger.warning(gu(f"{cdkey},已被兑换过了"))
                        time.sleep(1)
                        if auto.click_element("./assets/images/screen/cdkey/cdkey_clear.png", "image", 0.9, max_retries=5):
                            continue
                    elif auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=5):
                        logger.info(gu(f"{cdkey},兑换成功"))
                        time.sleep(1)
                        screen.change_to("cdkey")
                        continue
                        
        screen.change_to("menu")
