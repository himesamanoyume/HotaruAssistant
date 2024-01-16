# from module.config.config import Config
# from managers.notify_manager import notify
# from managers.logger_manager import logger
# from managers.config_manager import config
# from managers.screen_manager import screen
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
# from managers.automation_manager import auto
# from tasks.weekly.universe import Universe
# from tasks.weekly.forgottenhall import ForgottenHall
# import atexit
import pyuac
import glob
import shutil,sys,os
# from tasks.version.version import Version
# import pyperclip
import requests,json,time
# from datetime import datetime
# from module.config.config import Config
# config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
# task_mappings = json.load(open("./assets/config/task_mappings.json", 'r', encoding='utf-8'))

def removeLock():
    input("按回车开始执行...")
    import datetime
    while True:
        time.sleep(20)
        path = "./"
        for item in os.listdir(path):
            # print(path+item)
            if '.lock' in item:
                if os.path.isdir(path+item):
                    user = item.split(".lock")[0]
                    current_time = datetime.datetime.now()
                    print(f"[{current_time.hour:02d}:{current_time.minute:02d}]检测到lock文件夹：{item}")
                    if os.path.exists(path+user):
                        os.removedirs(path+item)
                        print(f"[{current_time.hour:02d}:{current_time.minute:02d}]已删除.lock")

def testFun():
    input("按回车开始执行...")
    
    input("...")

if __name__ == '__main__':
    testFun()
    # if not pyuac.isUserAdmin():
    #     try:
    #         pyuac.runAsAdmin(wait=False)
    #         sys.exit(0)
    #     except Exception:
    #         # logger.error("管理员权限获取失败")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    # else:
    #     try:
    #         testFun()
    #         # for i in range(10):
    #         #     testFun()
    #     except KeyboardInterrupt:
    #         # logger.error("发生错误: 手动强制停止")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    #     except Exception as e:
    #         # logger.error(f"发生错误: {e}")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    