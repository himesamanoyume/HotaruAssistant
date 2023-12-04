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
        logger.info(gu("开始进行累计施放2次秘技"))
        return HimekoTry.total(1)

    @staticmethod
    def item():
        logger.info(gu("开始进行累计击碎3个可破坏物"))
        return HimekoTry.total(2)

    @staticmethod
    def enemy_20():
        logger.info(gu("开始进行累计消灭20个敌人"))
        if config.daily_tasks[Utils.get_uid()]['累计消灭20个敌人']:
            logger.info(gu("【累计消灭20个敌人】已被顺带完成"))
            return True
        return HimekoTry.total() and HimekoTry.total()

    @staticmethod
    def weakness_to_fight():
        logger.info(gu("开始进行利用弱点进入战斗并获胜3次"))
        if config.daily_tasks[Utils.get_uid()]['利用弱点进入战斗并获胜3次']:
            logger.info(gu("【利用弱点进入战斗并获胜3次】已被顺带完成"))
            return True
        return HimekoTry.total() and HimekoTry.total()
    
    @staticmethod
    def total(endpoint:int=0):
        if config.daily_himeko_try_enable:
            screen.change_to("himeko_prepare")
            logger.info(gu("开始进行姬子试用"))
            auto.press_key(config.get_value("hotkey_technique"))
            time.sleep(2)
            auto.press_key(config.get_value("hotkey_technique"))
            time.sleep(2)
            # endpoint=0:一直进行到结束,1:使用两次秘技,2:破坏3次可破坏物
            if endpoint == 1:
                screen.change_to("himeko_try")
                return True
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
            if endpoint == 2:
                screen.change_to("himeko_try")
                return True
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
                        logger.info(gu("检测到战斗失败/重试"))
                        break
            
            time.sleep(1)

            auto.press_key("a")
            auto.press_key("a")
            auto.press_key("a")

            for i in range(20):
                if auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("姬子已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/herta_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("黑塔已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/natasha_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("娜塔莎已使用普攻"))
                    break

            time.sleep(3)
            auto.press_key("d")
            time.sleep(0.5)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/herta_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("黑塔已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("姬子已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/natasha_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("娜塔莎已使用普攻"))
                    break

            time.sleep(3)
            auto.press_key("a")
            for i in range(20):
                if auto.click_element("./assets/images/himeko/natasha_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("娜塔莎已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("姬子已使用普攻"))
                    break

            time.sleep(10)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("姬子已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/herta_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("黑塔已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/natasha_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("娜塔莎已使用普攻"))
                    break

            time.sleep(2)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/herta_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("黑塔已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("姬子已使用普攻"))
                    break
                elif auto.click_element("./assets/images/himeko/natasha_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("娜塔莎已使用普攻"))
                    break
            
            time.sleep(2)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/natasha_e.png", "image", 0.9, max_retries=10):
                    logger.info(gu("娜塔莎已激活战技"))
                    break
                else:
                    logger.info(gu("流程出现差错,重试"))
                    return HimekoTry.total(endpoint)

            time.sleep(2)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/natasha_active_q.png", "image", 0.9, max_retries=10):
                    logger.info(gu("娜塔莎已释放战技"))
                    break
                else:
                    logger.info(gu("流程出现差错,重试"))
                    return HimekoTry.total(endpoint)

            time.sleep(2)
            for i in range(20):
                if auto.find_element("./assets/images/himeko/himeko_skill.png", "image", 0.9, max_retries=20):
                    if auto.click_element("./assets/images/himeko/himeko_skill.png", "image", 0.9, max_retries=10):
                        logger.info(gu("姬子已开启终结技"))
                        break
                else:
                    logger.info(gu("流程出现差错,重试"))
                    return HimekoTry.total(endpoint)

            time.sleep(3)
            for i in range(20):
                if auto.click_element("./assets/images/himeko/himeko_space.png", "image", 0.9, max_retries=10):
                    logger.info(gu("姬子已施放终结技"))
                    break
                else:
                    logger.info(gu("流程出现差错,重试"))
                    return HimekoTry.total(endpoint)

            time.sleep(10)
            screen.change_to("himeko_try")
            return True
        else:
            logger.warning(gu("未开启姬子试用,跳过"))
            return False
