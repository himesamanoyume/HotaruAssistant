from managers.logger_manager import logger
from managers.config_manager import config
from managers.screen_manager import screen
import time
from datetime import datetime
from managers.translate_manager import _
from tasks.base.date import Date
from tasks.daily.photo import Photo
from tasks.daily.fight import Fight
from tasks.weekly.universe import Universe
from tasks.reward.reward import Reward
from tasks.daily.synthesis import Synthesis
from tasks.daily.utils import Utils
from tasks.weekly.forgottenhall import ForgottenHall
from tasks.weekly.echoofwar import Echoofwar
from tasks.power.power import Power
from tasks.daily.tasks import Tasks
from tasks.activity.activity import Activity
from tasks.daily.himekotry import HimekoTry



class Daily:


    def sub():

        if Utils.is_next_mon_4_am(config.echo_of_war_timestamp, Utils.get_uid()):
            config.save_config()
            if config.echo_of_war_enable:
                Echoofwar.start()
            else:
                logger.info(_("历战余响{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))
        else:
            logger.info(_("历战余响尚{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        Power.start()

        if Utils.is_next_4_am(config.fight_timestamp, Utils.get_uid()):
            config.save_config()
            if config.fight_enable:
                Fight.start()
            else:
                logger.info(_("锄大地{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))
        else:
            logger.info(_("锄大地尚{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        
        if config.universe_enable:
            # Power.start()
            # Reward.start()
            isTrue = Universe.start(get_reward=True, daily=True, nums=1)
            if isTrue:
                Power.start()
        else:
            logger.info(_("模拟宇宙{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))

        if Utils.is_next_mon_4_am(config.forgottenhall_timestamp, Utils.get_uid()):
            config.save_config()
            ForgottenHall.get_star_and_level()
            if config.forgottenhall_enable:
                ForgottenHall.start(Utils.get_uid())
            else:
                logger.info(_("忘却之庭{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))
        else:
            logger.info(_("忘却之庭尚{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        Reward.start()


    @staticmethod
    def start():
        if config.multi_login:
            logger.hr(_("多账号下开始日常任务"), 0)

        Utils.get_new_uid()
        Utils._content.update({'uid':Utils.get_uid()})
        Utils.getDailyScoreMappings()
        Tasks._isDetect = False
        if Utils.is_next_4_am(config.last_run_timestamp, Utils.get_uid()):
            config.save_config()
            logger.info(_("已是新的一天,开始每日"))
            # 活动
            Activity.start()

            screen.change_to("guide2")

            tasks = Tasks("./assets/config/task_mappings.json")
            tasks.start(Utils.get_uid())

            config.set_value("daily_tasks", tasks.daily_tasks)
            Utils.saveTimestamp('last_run_timestamp', Utils.get_uid())

        else:
            logger.info(_("日常任务{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        Utils.calcDailyTasksScore(Utils.get_uid())
        if len(config.daily_tasks[Utils.get_uid()]) > 0:
            task_functions = {
                "拍照1次": lambda: Photo.photograph(),
                "合成1次消耗品": lambda: Synthesis.consumables(),
                "合成1次材料": lambda: Synthesis.material(),
                "使用1件消耗品": lambda: Synthesis.use_consumables(),
                "完成1次「拟造花萼（金）」": lambda: Power.instance("拟造花萼（金）", config.instance_names[Utils.get_uid()]["拟造花萼（金）"], 10, 1),
                "完成1次「拟造花萼（赤）」": lambda: Power.instance("拟造花萼（赤）", config.instance_names[Utils.get_uid()]["拟造花萼（赤）"], 10, 1),
                "完成1次「凝滞虚影」": lambda: Power.instance("凝滞虚影", config.instance_names[Utils.get_uid()]["凝滞虚影"], 30, 1),
                "完成1次「侵蚀隧洞」": lambda: Power.instance("侵蚀隧洞", config.instance_names[Utils.get_uid()]["侵蚀隧洞"], 40, 1),
                "完成1次「历战余响」": lambda: Power.instance("历战余响", config.instance_names[Utils.get_uid()]["历战余响"], 30, 1),
                "累计施放2次秘技": lambda: HimekoTry.technique(),
                "累计击碎3个可破坏物": lambda: HimekoTry.item(),
                "完成1次「忘却之庭」": lambda: ForgottenHall.finish_forgottenhall(),
                "单场战斗中，触发3种不同属性的弱点击破": lambda: ForgottenHall.weakness_3(),
                "累计触发弱点击破效果5次": lambda: ForgottenHall.weakness_5(),
                "累计消灭20个敌人": lambda: ForgottenHall.enemy_20(),
                "利用弱点进入战斗并获胜3次": lambda: ForgottenHall.weakness_to_fight(),
                "施放终结技造成制胜一击1次": lambda: ForgottenHall.ultimate(),
                "通关「模拟宇宙」（任意世界）的1个区域": lambda: Universe.start(get_reward=False, nums=1, save=False),
            }

            logger.hr(_("今日实训"), 2)

            count = 0
            for key, value in config.daily_tasks[Utils.get_uid()].items():
                state = "\033[91m" + _("待完成") + "\033[0m" if value else "\033[92m" + _("已完成") + "\033[0m"
                logger.info(f"{key}: {state}")
                count = count + 1 if not value else count
            logger.info(_("已完成：{count_total}").format(count_total=f"\033[93m{count}/{len(config.daily_tasks[Utils.get_uid()])}\033[0m"))

            blacklist = {"单场战斗中，触发3种不同属性的弱点击破","累计触发弱点击破效果5次","利用弱点进入战斗并获胜3次","施放终结技造成制胜一击1次","累计消灭20个敌人"}

            for task_name, task_value in config.daily_tasks[Utils.get_uid()].items():
                if "{_task_name}".format(_task_name = task_name) in task_functions.keys():
                    if config.daily_tasks[Utils.get_uid()][task_name]:
                        if task_functions["{_task_name}".format(_task_name = task_name)]():
                            if task_name in blacklist:
                                continue
                            logger.info(_("{_task_name}已完成").format(_task_name=task_name))
                            config.daily_tasks[Utils.get_uid()][task_name] = False
                            Utils.showDailyTasksScore(task_name, Utils.get_uid())
                            # config.save_config()
                        else:
                            if not config.daily_tasks_fin[Utils.get_uid()]:
                                logger.warning(_("【{_task_name}】可能对应选项{red},请自行解决").format(_task_name=task_name, red="\033[91m" + _("未开启") + "\033[0m"))
                    else:
                        logger.info(_("【{_task_name}】该任务{green},跳过").format(_task_name=task_name, green="\033[92m" + _("已完成") + "\033[0m"))
                else:
                    logger.warning(_("【{_task_name}】可能该任务{red},或需要锄大地时顺带完成,请检查锄大地是否开启和根据情况自行解决").format(_task_name=task_name, red="\033[91m" + _("暂不直接支持") + "\033[0m"))                                              

            logger.hr(_("每日部分结束"), 2)

            count = 0
            for key, value in config.daily_tasks[Utils.get_uid()].items():
                count = count + 1 if not value else count

            logger.info(_("已完成：{count_total}").format(count_total=f"\033[93m{count}/{len(config.daily_tasks[Utils.get_uid()])}\033[0m"))
        
        Utils.calcDailyTasksScore(Utils.get_uid())
        logger.hr(_("完成"), 2)
        Daily.sub()
        totalTime = time.time() - Utils._start_timestamp
        _day = int(totalTime // 86400)
        _hour = int((totalTime - _day * 86400) // 3600)
        _minute = int(((totalTime - _day *86400) - _hour * 3600) // 60)
        _second = int(((totalTime - _day *86400) - _hour * 3600) - _minute * 60)
        Utils._content['running_time'] = (f"{_day}天" if not _day == 0 else '') + (f"{_hour}时" if not _hour == 0 else '') + (f"{_minute}分" if not _minute == 0 else '') + f"{_second}秒"
        logger.info(f"本次运行时长:{Utils._content['running_time']}")
        Utils.calcDailyTasksScore(Utils.get_uid())
