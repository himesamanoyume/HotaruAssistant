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
    instance_name = "蛀星的旧靥"
    instance_name = instance_name.replace("巽风之形", "风之形")
    instance_name = instance_name.replace("翼风之形", "风之形")

    instance_name = instance_name.replace("偃偶之形", "偶之形")
    instance_name = instance_name.replace("孽兽之形", "兽之形")

    instance_name = instance_name.replace("燔灼之形", "灼之形")
    instance_name = instance_name.replace("潘灼之形", "灼之形")
    instance_name = instance_name.replace("熠灼之形", "灼之形")
    instance_name = instance_name.replace("蛀星的旧靥", "蛀星的旧")


    screen.change_to('guide3')
    instance_type_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
    if not auto.click_element("历战余响", "text", crop=instance_type_crop):
        if auto.click_element("侵蚀隧洞", "text", max_retries=10, crop=instance_type_crop):
            auto.mouse_scroll(12, -1)
            time.sleep(0.5)
            auto.click_element("历战余响", "text", crop=instance_type_crop)
    # 截图过快会导致结果不可信
    time.sleep(1)

    # 传送
    instance_name_crop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
    auto.click_element("./assets/images/screen/guide/power.png", "image", max_retries=10)
    Flag = False
    for i in range(7):
        if auto.click_element("传送", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name):
            Flag = True
            break
        if auto.click_element("追踪", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name):
            nowtime = time.time()
            logger.error(f"{nowtime},{instance_name}:你似乎没有解锁这个副本?总之无法传送到该副本")
        auto.mouse_scroll(18, -1)
        # 等待界面完全停止
        time.sleep(1)
        
    
    if not Flag:
        logger.error("⚠️刷副本未完成 - 没有找到指定副本名称⚠️")
        # Base.send_notification_with_screenshot(_("⚠️刷副本未完成 - 没有找到指定副本名称⚠️"))
        return False
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
    