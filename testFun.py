# from module.config.config import Config
# from managers.notify_manager import notify
from managers.logger_manager import logger
# from managers.config_manager import config
from managers.screen_manager import screen
# from tasks.power.power import Power
from managers.utils_manager import gu
# from managers.ocr_manager import ocr
# from managers.translate_manager import _
# from tasks.game.game import Game
# from tasks.daily.daily import Daily
# from tasks.daily.fight import Fight
from tasks.daily.utils import Utils
# from datetime import datetime
# import questionary
from tasks.base.windowswitcher import WindowSwitcher
from managers.automation_manager import auto
# from tasks.weekly.universe import Universe
# from tasks.weekly.forgottenhall import ForgottenHall
import atexit
import pyuac
import glob
import shutil,sys,os
# from tasks.version.version import Version
import pyperclip
import requests,json,time
# from datetime import datetime
from module.config.config import Config
config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
task_mappings = json.load(open("./assets/config/task_mappings.json", 'r', encoding='utf-8'))

def testFun():
    input("按回车开始执行...")
    WindowSwitcher.check_and_switch(config.game_title_name)
    # ------------------------------------------------------------------------
    screen.change_to('bag_relics')
    if auto.click_element("分解", "text", max_retries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
        if auto.click_element("分解", "text", max_retries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
            time.sleep(1)
            if auto.click_element("./assets/images/relic/fast_select.png", "image", 0.9, max_retries=10):
                # 等待筛选界面弹出
                time.sleep(1)
                fast_select_crop=(439.0 / 1920, 357.0 / 1080, 1018.0 / 1920, 448.0 / 1080)
                auto.click_element("全选已弃置", "text", max_retries=10, crop=fast_select_crop)
                time.sleep(0.5)
                auto.click_element("3星及以下", "text", max_retries=10, crop=fast_select_crop)
                time.sleep(0.5)
                if config.relic_salvage_4star_enable[Utils.get_uid()]:
                    auto.click_element("4星及以下", "text", max_retries=10, crop=fast_select_crop)
                    time.sleep(0.5)
                if config.relic_salvage_5star_enable[Utils.get_uid()]:
                    auto.click_element("5星及以下", "text", max_retries=10, crop=fast_select_crop)
                    time.sleep(0.5)
                if auto.click_element("确认", "text", max_retries=10, crop=fast_select_crop):
                    time.sleep(3)
                    countText = auto.get_single_line_text((616.0 / 1920, 871.0 / 1080, 110.0 / 1920, 37.0 / 1080), [], 5)
                    count = countText.split('/')[0]
                    logger.info(gu(f"已选数量:{count}/500"))
                    time.sleep(0.5)
                    if count != 0:
                        if config.relic_salvage_5star_enable[Utils.get_uid()] and config.relic_salvage_5star_to_exp[Utils.get_uid()]:
                            if auto.click_element("./assets/images/relic/relic_exp.png", "image", 0.9, max_retries=10):
                                logger.info("已点击将5星遗器分解为遗器经验材料")
                        time.sleep(1)
                        if auto.click_element("./assets/images/relic/salvage.png", "image", max_retries=10):
                            logger.info(gu(f"已点击分解遗器"))
                            time.sleep(1)
                            if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=10):
                                logger.info(gu(f"已点击确认"))
                                time.sleep(1)
                                if auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10):
                                    logger.info(gu(f"已点击关闭窗口"))
                                    time.sleep(1)
                                    logger.info(gu(f"分解遗器{count}件完成"))
                                    screen.change_to('main')
                                    return True
                    else:
                        logger.error(gu("分解遗器失败: 没有多余的遗器可供分解"))
                        screen.change_to('main')
                        return False
    logger.error(gu("分解遗器失败"))
    # ------------------------------------------------------------------------
    input("...")

if __name__ == '__main__':
    # testFun()
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            # logger.error("管理员权限获取失败")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            testFun()
            # for i in range(10):
            #     testFun()
        except KeyboardInterrupt:
            # logger.error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            # logger.error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    