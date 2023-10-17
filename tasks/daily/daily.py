from managers.logger_manager import logger
from managers.config_manager import config
from managers.screen_manager import screen
import time
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



class Daily:


    def sub(uid):

        Utils.detectTimestamp(config.echo_of_war_timestamp, uid)

        if Date.is_next_mon_4_am(config.echo_of_war_timestamp[uid]):
            if config.echo_of_war_enable:
                Echoofwar.start(uid)
            else:
                logger.info(_("历战余响未开启"))
        else:
            logger.info(_("历战余响尚未刷新"))

        Power.start()

        Utils.detectTimestamp(config.fight_timestamp, uid)

        if Date.is_next_4_am(config.fight_timestamp[uid]):
            if config.fight_enable:
                Fight.start(uid)
            else:
                logger.info(_("锄大地未开启"))
        else:
            logger.info(_("锄大地尚未刷新"))

        Utils.detectTimestamp(config.universe_timestamp, uid)

        if Date.is_next_mon_4_am(config.universe_timestamp[uid]):
            if config.universe_enable:
                Power.start()
                Reward.start()
                Universe.start(uid, get_reward=True)
                Power.start()
            else:
                logger.info(_("模拟宇宙未开启"))
        else:
            logger.info(_("模拟宇宙尚未刷新"))

        Utils.detectTimestamp(config.forgottenhall_timestamp, uid)

        if Date.is_next_mon_4_am(config.forgottenhall_timestamp[uid]):
            if config.forgottenhall_enable:
                ForgottenHall.start(uid)
            else:
                logger.info(_("忘却之庭未开启"))
        else:
            logger.info(_("忘却之庭尚未刷新"))

        Reward.start()

    @staticmethod
    def start(uid):
        if config.multi_login:
            logger.hr(_("多账号下开始日常任务"), 0)

            Utils.detectTimestamp(config.last_run_timestamp, uid)

            if Date.is_next_4_am(config.last_run_timestamp[uid]):
                logger.info(_("已是新的一天,开始每日"))
                # 活动
                Activity.start()

                screen.change_to("guide2")

                tasks = Tasks("./assets/config/task_mappings.json")
                tasks.start(uid)

                config.set_value("daily_tasks", tasks.daily_tasks)
                Utils.saveTimestamp(config.last_run_timestamp, uid)

            else:
                logger.info(_("日常任务尚未刷新"))

            if len(config.daily_tasks[uid]) > 0:
                task_functions = {
                    "拍照1次": lambda: Photo.photograph(),
                    "合成1次消耗品": lambda: Synthesis.consumables(),
                    "合成1次材料": lambda: Synthesis.material(),
                    "使用1件消耗品": lambda: Synthesis.use_consumables(),
                    "完成1次「拟造花萼（金）」": lambda: Power.instance("拟造花萼（金）", config.instance_names["拟造花萼（金）"], 10, 1),
                    "完成1次「拟造花萼（赤）」": lambda: Power.instance("拟造花萼（赤）", config.instance_names["拟造花萼（赤）"], 10, 1),
                    "完成1次「凝滞虚影」": lambda: Power.instance("凝滞虚影", config.instance_names["凝滞虚影"], 30, 1),
                    "完成1次「侵蚀隧洞」": lambda: Power.instance("侵蚀隧洞", config.instance_names["侵蚀隧洞"], 40, 1),
                    "完成1次「历战余响」": lambda: Power.instance("历战余响", config.instance_names["历战余响"], 30, 1),
                    "完成1次「忘却之庭」": lambda: ForgottenHall.start_daily(),
                }

                logger.hr(_("今日实训"), 2)
                count = 0
                for key, value in config.daily_tasks[uid].items():
                    state = "\033[91m" + _("待完成") + "\033[0m" if value else "\033[92m" + _("已完成") + "\033[0m"
                    logger.info(f"{key}: {state}")
                    count = count + 1 if not value else count
                # logger.info(_("已完成：{count}/{total}").format(count=count, total=len(config.daily_tasks)))
                logger.info(_("已完成：{count_total}").format(count_total=f"\033[93m{count}/{len(config.daily_tasks[uid])}\033[0m"))

                
                for task_name, task_value in config.daily_tasks[uid].items():
                    if "{_task_name}".format(_task_name = task_name) in task_functions.keys():
                        if config.daily_tasks[uid][task_name]:
                            if task_functions["{_task_name}".format(_task_name = task_name)]():
                                logger.info(_("{_task_name}已完成").format(_task_name=task_name))
                                config.daily_tasks[uid][task_name] = False
                                config.save_config()
                            else:
                                logger.warning(_("【{_task_name}】可能对应选项{red},请自行解决").format(_task_name=task_name, red="\033[91m" + _("未开启") + "\033[0m"))
                        else:
                            logger.warning(_("【{_task_name}】该任务{green},跳过").format(_task_name=task_name, green="\033[92m" + _("已完成") + "\033[0m"))
                    else:
                        logger.warning(_("【{_task_name}】可能该任务{red},请自行解决").format(_task_name=task_name, red="\033[91m" + _("暂不支持") + "\033[0m"))                                              

                # logger.info(_("进入task_functions.items()循环"))
                # for task_name, task_function in task_functions.items():
                #     if task_name in config.daily_tasks[uid] and config.daily_tasks[uid][task_name]:
                #         if task_function():
                #             logger.info(_("{_task_name}已完成").format(_task_name=task_name))
                #             config.daily_tasks[uid][task_name] = False
                #             config.save_config()
                #         else:
                #             logger.warning(_("{_task_name}可能选项未开启,请自行解决").format(_task_name=task_name))

                logger.hr(_("每日部分结束"), 2)

                count = 0
                for key, value in config.daily_tasks[uid].items():
                    state = "\033[91m" + _("待完成") + "\033[0m" if value else "\033[92m" + _("已完成") + "\033[0m"
                    logger.info(f"{key}: {state}")
                    count = count + 1 if not value else count
                # logger.info(_("已完成：{count}/{total}").format(count=count, total=len(config.daily_tasks)))
                logger.info(_("已完成：{count_total}").format(count_total=f"\033[93m{count}/{len(config.daily_tasks[uid])}\033[0m"))


                logger.hr(_("完成"), 2)
            Daily.sub(uid)
        else:
            logger.hr(_("开始日常任务"), 0)

            Utils.detectTimestamp(config.last_run_timestamp, 1)

            if Date.is_next_4_am(config.last_run_timestamp[1]):

                # 活动
                Activity.start()

                screen.change_to("guide2")

                tasks = Tasks("./assets/config/task_mappings.json")
                tasks.start()

                config.set_value("daily_tasks", tasks.daily_tasks)

                Utils.saveTimestamp(config.last_run_timestamp, 1)
            else:
                logger.info(_("日常任务尚未刷新"))

            if len(config.daily_tasks) > 0:
                task_functions = {
                    "拍照1次": lambda: Photo.photograph(),
                    "合成1次消耗品": lambda: Synthesis.consumables(),
                    "合成1次材料": lambda: Synthesis.material(),
                    "使用1件消耗品": lambda: Synthesis.use_consumables(),
                    "完成1次「拟造花萼（金）」": lambda: Power.instance("拟造花萼（金）", config.instance_names["拟造花萼（金）"], 10, 1),
                    "完成1次「拟造花萼（赤）」": lambda: Power.instance("拟造花萼（赤）", config.instance_names["拟造花萼（赤）"], 10, 1),
                    "完成1次「凝滞虚影」": lambda: Power.instance("凝滞虚影", config.instance_names["凝滞虚影"], 30, 1),
                    "完成1次「侵蚀隧洞」": lambda: Power.instance("侵蚀隧洞", config.instance_names["侵蚀隧洞"], 40, 1),
                    "完成1次「历战余响」": lambda: Power.instance("历战余响", config.instance_names["历战余响"], 30, 1),
                    "完成1次「忘却之庭」": lambda: ForgottenHall.start_daily(),
                }

                logger.hr(_("今日实训"), 2)
                count = 0
                for key, value in config.daily_tasks.items():
                    state = "\033[91m" + _("待完成") + "\033[0m" if value else "\033[92m" + _("已完成") + "\033[0m"
                    logger.info(f"{key}: {state}")
                    count = count + 1 if not value else count
                # logger.info(_("已完成：{count}/{total}").format(count=count, total=len(config.daily_tasks)))
                logger.info(_("已完成：{count_total}").format(count_total=f"\033[93m{count}/{len(config.daily_tasks)}\033[0m"))

                for task_name, task_function in task_functions.items():
                    if task_name in config.daily_tasks and config.daily_tasks[task_name]:
                        if task_function():
                            config.daily_tasks[task_name] = False
                            config.save_config()

                logger.hr(_("完成"), 2)
            Daily.sub(1)

    