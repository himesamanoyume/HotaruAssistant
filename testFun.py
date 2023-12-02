from managers.config_manager import config
from managers.translate_manager import _
from managers.screen_manager import screen
from managers.logger_manager import logger
from managers.utils_manager import gu
from managers.automation_manager import auto
import time,atexit,sys,pyuac

def testFun():
    if config.daily_himeko_try_enable:
        screen.change_to("himeko_prepare")
        logger.info(gu("开始进行姬子试用"))
        auto.press_key(config.get_value("hotkey_technique"))
        time.sleep(2)
        auto.press_key(config.get_value("hotkey_technique"))
        time.sleep(2)
        # endpoint=0:一直进行到结束,1:使用两次秘技,2:破坏3次可破坏物
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
        time.sleep(3)
        auto.press_key("d")

        for i in range(20):
            if auto.click_element("./assets/images/himeko/herta_q.png", "image", 0.9, max_retries=10):
                logger.info(gu("黑塔已使用普攻"))
                break
        time.sleep(3)
        auto.press_key("a")
        for i in range(20):
            if auto.click_element("./assets/images/himeko/natasha_q.png", "image", 0.9, max_retries=10):
                logger.info(gu("娜塔莎已使用普攻"))
                break

        time.sleep(10)
        for i in range(20):
            if auto.click_element("./assets/images/himeko/himeko_q.png", "image", 0.9, max_retries=10):
                logger.info(gu("姬子已使用普攻"))
                break

        time.sleep(3)
        for i in range(20):
            if auto.click_element("./assets/images/himeko/himeko_skill.png", "image", 0.9, max_retries=10):
                logger.info(gu("姬子已开启终结技"))
                break
        time.sleep(3)
        for i in range(20):
            if auto.click_element("./assets/images/himeko/himeko_space.png", "image", 0.9, max_retries=10):
                logger.info(gu("姬子已施放终结技"))
                break

        time.sleep(10)
        screen.change_to("himeko_try")
        return True

if __name__ == '__main__':
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logger.error("管理员权限获取失败")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            testFun()
        except KeyboardInterrupt:
            logger.error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logger.error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    