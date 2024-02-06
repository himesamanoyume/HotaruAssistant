# from module.config.config import Config
# from managers.notify_manager import notify
# from managers.logger_manager import logger
# from managers.config_manager import config
from managers.screen_manager import screen
# from tasks.power.power import Power
# from managers.utils_manager import gu
# from managers.ocr_manager import ocr
# from managers.translate_manager import _
# from tasks.game.game import Game
# from tasks.daily.daily import Daily
# from tasks.daily.fight import Fight
# from tasks.daily.utils import Utils
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
    instance_type = "凝滞虚影"
    instance_name = "空海之形"

    screen.change_to('guide3')
    instance_type_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
    if not auto.click_element(instance_type, "text", crop=instance_type_crop):
        if auto.click_element("侵蚀隧洞", "text", max_retries=10, crop=instance_type_crop):
            auto.mouse_scroll(12, -1)
            time.sleep(0.5)
            auto.click_element(instance_type, "text", crop=instance_type_crop)
    # 截图过快会导致结果不可信
    time.sleep(1)

    # 传送
    instance_name_crop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
    auto.click_element("./assets/images/screen/guide/power.png", "image", max_retries=10)
    Flag = False
    if instance_type in ['拟造花萼（赤）']:
        import json
        rb = open("./assets/config/ruby_detail.json", 'r', encoding='utf-8')
        ruby = json.load(rb)
        rb.close()
        for i in range(7):
            point = auto.find_element(f"./assets/images/screen/guide/aka/{ruby['拟造花萼（赤）'][instance_name]}.png", "image", 0.9, max_retries=5)

            success_point_top_left_x = point[0][0]
            success_point_top_left_y = point[0][1]
            text_crop=(success_point_top_left_x/ 1920, success_point_top_left_y / 1080, 735 / 1920, 87 / 1080)

            if auto.click_element("传送", "text", crop=text_crop):
                Flag = True
                break
            
            if auto.click_element("追踪", "text", crop=text_crop):
                print("你似乎没有解锁这个副本?总之无法传送到该副本")
                # nowtime = time.time()
                # logger.error(gu(f"{nowtime},{instance_name}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                # raise Exception(f"{nowtime},{instance_name}:你似乎没有解锁这个副本?总之无法传送到该副本")
            auto.mouse_scroll(18, -1)
            # 等待界面完全停止
            time.sleep(1)
    else:
        for i in range(7):
            if auto.click_element("传送", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name):
                Flag = True
                break
            if auto.click_element("追踪", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name):
                print("你似乎没有解锁这个副本?总之无法传送到该副本")
                # nowtime = time.time()
                # logger.error(gu(f"{nowtime},{instance_name}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                # raise Exception(f"{nowtime},{instance_name}:你似乎没有解锁这个副本?总之无法传送到该副本")
            auto.mouse_scroll(18, -1)
            # 等待界面完全停止
            time.sleep(1)
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
    