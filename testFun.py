from managers.config_manager import config
from managers.translate_manager import _
from managers.screen_manager import screen
from managers.logger_manager import logger
from managers.utils_manager import gu
from managers.automation_manager import auto
import time,atexit,sys,pyuac

def testFun(type=2):
    css = open("./static/css/common.css", 'r', encoding='utf-8')
    htmlStyle = css.read()
    css.close()

if __name__ == '__main__':
    testFun()
    # if not pyuac.isUserAdmin():
    #     try:
    #         pyuac.runAsAdmin(wait=False)
    #         sys.exit(0)
    #     except Exception:
    #         logger.error("管理员权限获取失败")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    # else:
    #     try:
    #         for i in range(10):
    #             testFun()
    #     except KeyboardInterrupt:
    #         logger.error("发生错误: 手动强制停止")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    #     except Exception as e:
    #         logger.error(f"发生错误: {e}")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    