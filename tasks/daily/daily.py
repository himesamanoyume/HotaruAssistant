from managers.logger_manager import logger
from managers.config_manager import config
from managers.automation_manager import auto
from managers.screen_manager import screen
import time
from managers.translate_manager import _
from tasks.base.date import Date
from tasks.daily.photo import Photo
from tasks.daily.fight import Fight
from tasks.weekly.universe import Universe
from tasks.reward.reward import Reward
from tasks.reward.dispatch import Dispatch
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
                logger.info(_("历战余响{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))
        else:
            logger.info(_("历战余响尚{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        Power.start()

        Utils.detectTimestamp(config.fight_timestamp, uid)

        if Date.is_next_4_am(config.fight_timestamp[uid]):
            if config.fight_enable:
                Fight.start(uid)
            else:
                logger.info(_("锄大地{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))
        else:
            logger.info(_("锄大地尚{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        Utils.detectTimestamp(config.universe_timestamp, uid)

        if Date.is_next_mon_4_am(config.universe_timestamp[uid]):
            if config.universe_enable:
                Power.start()
                Reward.start(uid)
                Universe.start(uid, get_reward=True)
                Power.start()
            else:
                logger.info(_("模拟宇宙{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))
        else:
            logger.info(_("模拟宇宙尚{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        Utils.detectTimestamp(config.forgottenhall_timestamp, uid)

        if Date.is_next_mon_4_am(config.forgottenhall_timestamp[uid]):
            if config.forgottenhall_enable:
                ForgottenHall.start(uid)
            else:
                logger.info(_("忘却之庭{red}".format(red="\033[91m" + _("未开启") + "\033[0m")))
        else:
            logger.info(_("忘却之庭尚{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

        Reward.start(uid)

    def get_uid(crop):
        try:
            uid = auto.get_single_line_text(crop=crop, blacklist=[], max_retries=9)
            logger.info(_(f"识别到UID为:{uid}"))
            return uid
        except Exception as e:
            logger.error(_("识别UID失败: {error}").format(error=e))
            return -1

    @staticmethod
    def start():
        uid_crop = (68.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080)
        uid = Daily.get_uid(uid_crop)
        if uid == -1:
            logger.warning(_("因读取UID失败,程序中止"))
            return
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
            Utils.saveTimestamp('last_run_timestamp', uid)

        else:
            logger.info(_("日常任务{red}".format(red="\033[91m" + _("未刷新") + "\033[0m")))

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
                "派遣1次委托": lambda: Dispatch.get_reward(),
            }

            logger.hr(_("今日实训"), 2)

            count = 0
            for key, value in config.daily_tasks[uid].items():
                state = "\033[91m" + _("待完成") + "\033[0m" if value else "\033[92m" + _("已完成") + "\033[0m"
                logger.info(f"{key}: {state}")
                count = count + 1 if not value else count
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
                        logger.info(_("【{_task_name}】该任务{green},跳过").format(_task_name=task_name, green="\033[92m" + _("已完成") + "\033[0m"))
                else:
                    logger.warning(_("【{_task_name}】可能该任务{red},或需要锄大地时顺带完成,请检查锄大地是否开启和根据情况自行解决").format(_task_name=task_name, red="\033[91m" + _("暂不直接支持") + "\033[0m"))                                              

            logger.hr(_("每日部分结束"), 2)

            count = 0
            for key, value in config.daily_tasks[uid].items():
                count = count + 1 if not value else count

            logger.info(_("已完成：{count_total}").format(count_total=f"\033[93m{count}/{len(config.daily_tasks[uid])}\033[0m"))
        
        logger.hr(_("完成"), 2)
        Daily.sub(uid)
