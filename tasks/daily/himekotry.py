from managers.config_manager import config
from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.utils_manager import gu
from managers.logger_manager import logger
from tasks.reward.reward import Reward
from tasks.daily.utils import Utils
import time


class HimekoTry:
    @staticmethod
    def technique():
        HimekoTry.total()

    @staticmethod
    def item():
        HimekoTry.total()

    @staticmethod
    def enemy_20():
        for i in range(2):
            if config.daily_tasks[Utils.get_uid()]['累计消灭20个敌人']:
                break
            HimekoTry.total()
        return True

    @staticmethod
    def weakness_to_fight():
        for i in range(3):
            if config.daily_tasks[Utils.get_uid()]['利用弱点进入战斗并获胜3次']:
                break
            HimekoTry.total()
        return True
    
    @staticmethod
    def total():
        if config.daily_himeko_try_enable:
            screen.change_to("himeko_prepare")
            auto.press_key(config.get_value("hotkey_technique"))
            time.sleep(2)
            auto.press_key(config.get_value("hotkey_technique"))
            time.sleep(2)
            auto.press_key("w", 6)
            auto.press_mouse()
            time.sleep(1)
            auto.press_key("d", 2)
            auto.press_key("s", 2)
            auto.press_mouse()
            time.sleep(1)
            auto.press_key("w", 0.5)
            auto.press_key("d", 2)
            auto.press_mouse()
            time.sleep(1)
            auto.press_key("w", 2)
            auto.press_mouse()
            time.sleep(3)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/close.png", "image", 0.9, max_retries=10):
                    break
            time.sleep(1)
            for i in range(20):
                if auto.find_element("./assets/images/base/2x_speed_on.png", "image", 0.9, crop=(1618.0 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
                    logger.info(gu("二倍速已开启"))
                    break
                else:
                    logger.info(gu("尝试开启二倍速"))
                    auto.press_key("b")
                    time.sleep(0.5)
                    if auto.find_element("./assets/images/fight/fight_again.png", "image", 0.9) or auto.find_element("./assets/images/fight/fight_fail.png", "image", 0.9):
                        break
            
            time.sleep(1)
            auto.press_key("a")
            auto.press_key("a")
            auto.press_key("a")
            for i in range(20):
                if auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                    break
            time.sleep(3)
            auto.press_key("d")

            for i in range(20):
                if auto.click_element("./assets/images/himeko/herta_q.png", "image", 0.9, max_retries=10):
                    break
            time.sleep(3)
            auto.press_key("a")
            for i in range(20):
                if auto.click_element("./assets/images/himeko/natasha_q.png", "image", 0.9, max_retries=10):
                    break

            time.sleep(10)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                    break

            time.sleep(3)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/himeko_skill.png", "image", 0.9, max_retries=10):
                    break
            time.sleep(3)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/himeko_space.png", "image", 0.9, max_retries=10):
                    break

            time.sleep(10)
            screen.change_to("himeko_try")
            Reward.start()
            return True
