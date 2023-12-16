from module.config.config import Config
from managers.notify_manager import notify
from managers.logger_manager import logger
from managers.config_manager import config
from managers.screen_manager import screen
from managers.utils_manager import gu
from managers.ocr_manager import ocr
from managers.translate_manager import _
from tasks.game.game import Game
from tasks.daily.daily import Daily
from tasks.daily.fight import Fight
from tasks.daily.utils import Utils
from datetime import datetime
import questionary
from managers.automation_manager import auto
import time
from tasks.weekly.universe import Universe
from tasks.weekly.forgottenhall import ForgottenHall
import atexit
import pyuac
import glob
import shutil,sys
from tasks.version.version import Version
import pyperclip

def testFun():
    input("...")
    screen.change_to("cdkey")
    config.reload()
    for cdkey in config.cdkey_list:
        time.sleep(1)
        logger.info(cdkey)
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
    input("...")

    

if __name__ == '__main__':
    # testFun()
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
            for i in range(10):
                testFun()
        except KeyboardInterrupt:
            logger.error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logger.error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    