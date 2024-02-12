from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.config_manager import config
from managers.logger_manager import logger
from managers.translate_manager import _
from managers.utils_manager import gu

class Assist:
    @staticmethod
    def get_reward():
        if not config.assist_enable:
            logger.info(gu("支援奖励未开启"))
            return False

        screen.change_to('visa')
        if auto.click_element("./assets/images/assist/gift.png", "image", 0.9):
            auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10)
