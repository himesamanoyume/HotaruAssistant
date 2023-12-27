# from module.config.config import Config
# from managers.notify_manager import notify
from managers.logger_manager import logger
# from managers.config_manager import config
from managers.screen_manager import screen
from tasks.power.power import Power
# from managers.utils_manager import gu
from managers.ocr_manager import ocr
# from managers.translate_manager import _
# from tasks.game.game import Game
# from tasks.daily.daily import Daily
# from tasks.daily.fight import Fight
# from tasks.daily.utils import Utils
# from datetime import datetime
# import questionary
from managers.automation_manager import auto
# import time
# from tasks.weekly.universe import Universe
# from tasks.weekly.forgottenhall import ForgottenHall
# import atexit
import pyuac
import glob
import shutil,sys
# from tasks.version.version import Version
# import pyperclip
import requests,json
from datetime import datetime
import time

task_mappings = json.load(open("./assets/config/task_mappings.json", 'r', encoding='utf-8'))

def testFun():
    input("...")
    relic_name_crop=(783.0 / 1920, 318.0 / 1080, 436.0 / 1920, 53.0 / 1080) # 遗器名称
    relic_prop_crop=(831.0 / 1920, 398.0 / 1080, 651.0 / 1920, 181.0 / 1080) # 遗器属性
    logger.info(("开始检测遗器"))
    point = auto.find_element("./assets/images/fight/fight_reward.png", "image", 0.9,max_retries=2)
    success_reward_top_left_x = point[0][0]
    success_reward_top_left_y = point[0][1]
    logger.info((f"{success_reward_top_left_x},{success_reward_top_left_y}"))
    for i in range(2):
        for j in range(7):
            if auto.click_element("./assets/images/fight/relic.png", "image", 0.9, max_retries=2, crop=((success_reward_top_left_x - 420 + j*120.0 )/ 1920, (success_reward_top_left_y + 30 + i*120) / 1080, 120.0 / 1920, 120.0 / 1080)):
                time.sleep(1.5)
                if auto.click_element("./assets/images/fight/relic_info_close.png", "image", 0.9, max_retries=3):
                            time.sleep(0.5)
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
    