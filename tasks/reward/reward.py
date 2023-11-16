from managers.logger_manager import logger
from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.translate_manager import _
from tasks.reward.mail import Mail
from managers.utils_manager import gu
from tasks.reward.assist import Assist
from tasks.daily.utils import Utils
from tasks.reward.dispatch import Dispatch
from tasks.reward.quest import Quest
from tasks.reward.srpass import SRPass


class Reward:
    @staticmethod
    def start():
        logger.hr(_("开始领奖励"), 0)
        screen.change_to('menu')

        reward_list = []

        reward_mapping = {
            "mail": lambda: auto.find_element("./assets/images/menu/mail_reward.png", "image", 0.9, take_screenshot=False, crop=(0.95, 0.1, 0.05, 0.6)),
            "assist": lambda: auto.find_element("./assets/images/menu/assist_reward.png", "image", 0.9, take_screenshot=False),
            "dispatch": lambda: auto.find_element("./assets/images/menu/dispatch_reward.png", "image", 0.95, take_screenshot=False),
            # "quest": lambda: auto.find_element("./assets/images/menu/quest_reward.png", "image", 0.95, take_screenshot=False),
            # "srpass": lambda: auto.find_element("./assets/images/menu/pass_reward.png", "image", 0.95, take_screenshot=False),
        }

        for reward_name, reward_function in reward_mapping.items():
            if reward_function():
                reward_list.append(reward_name)

        flag = False
        if len(reward_list) != 0:
            flag = True
            if "mail" in reward_list:
                logger.hr(_("检测到邮件奖励"), 2)
                Mail.get_reward()
                logger.info(gu("邮件奖励完成"))
            if "assist" in reward_list:
                logger.hr(_("检测到支援奖励"), 2)
                Assist.get_reward()
                logger.info(gu("支援奖励完成"))
            if "dispatch" in reward_list:
                logger.hr(_("检测到委托奖励"), 2)
                Dispatch.get_reward(Utils.get_uid())
                logger.info(gu("委托奖励完成"))

        # 每日实训和无名勋礼需要实时检测
        screen.change_to('menu')
        if auto.find_element("./assets/images/menu/quest_reward.png", "image", 0.95):
            flag = True
            logger.hr(_("检测到每日实训奖励"), 2)
            Quest.get_reward()
            logger.info(gu("领取每日实训奖励完成"))
        screen.change_to('menu')
        if auto.find_element("./assets/images/menu/pass_reward.png", "image", 0.95):
            flag = True
            logger.hr(_("检测到无名勋礼奖励"), 2)
            SRPass.get_reward()
            logger.info(gu("领取无名勋礼奖励完成"))

        if not flag:
            logger.info(gu("未检测到任何奖励"))

        logger.hr(_("完成"), 2)
