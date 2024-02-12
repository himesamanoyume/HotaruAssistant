from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.logger_manager import logger
from managers.translate_manager import _
from managers.utils_manager import gu
from tasks.base.base import Base
import time


class SRPass:
    @staticmethod
    def get_reward():
        # 先判断是否能领取经验
        screen.change_to('pass2')
        time.sleep(1)
        if auto.click_element("./assets/images/pass/one_key_receive.png", "image", 0.9):
            # 等待可能出现的升级动画
            time.sleep(2)
        screen.change_to('pass1')
        time.sleep(1)
        # 判断是否解锁了"无名客的荣勋"
        if auto.find_element("./assets/images/pass/lock.png", "image", 0.9):
            time.sleep(1)
            # 若没解锁则领取奖励
            if auto.click_element("./assets/images/pass/one_key_receive.png", "image", 0.9):
                time.sleep(1)
                auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10)
                time.sleep(1)
        
        time.sleep(1)
        # 判断是否满级
        if auto.find_element("./assets/images/pass/50.png", "image", 0.9):
            logger.info(gu("🎉当前版本无名勋礼已满级🎉"))
            # Base.send_notification_with_screenshot(_("🎉当前版本无名勋礼已满级🎉"))
