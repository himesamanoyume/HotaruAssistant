import os
import sys
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from managers.notify_manager import notify
from managers.logger_manager import logger
from managers.config_manager import config
from managers.ocr_manager import ocr
from managers.translate_manager import _
from tasks.game.game import Game
from tasks.game.stop import Stop
from tasks.daily.daily import Daily
from tasks.daily.fight import Fight
from tasks.daily.utils import Utils
import questionary
from tasks.version.version import Version
from tasks.weekly.universe import Universe
from tasks.weekly.forgottenhall import ForgottenHall
import atexit
import pyuac
import sys


def main(action=None):
    # 免责申明
    if not config.agreed_to_disclaimer:
        logger.error(_("您尚未同意《免责声明》"))
        input(_("按回车键关闭窗口. . ."))
        sys.exit(0)
    if config.multi_login:
        # 多账号
        if len(config.multi_login_accounts) == 0:
            logger.warning(_("你并没有填写注册表位置"))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(0)
        else:
            logger.info(_("开始多账号运行"))

            options_reg = dict()
            for index in range(len(config.multi_login_accounts)):
                uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
                Utils.init_instanceButNoSave(uidStr)

                if Utils.is_next_4_am(config.last_run_timestamp, uidStr, False):
                    Utils.detectIsNoneButNoSave(config.daily_tasks_score, uidStr)
                    Utils.detectIsNoneButNoSave(config.daily_tasks_fin, uidStr, False)
                    config.daily_tasks_score[uidStr] = 0
                    config.daily_tasks_fin[uidStr] = False
                    

                if Utils.is_next_mon_4_am(config.universe_timestamp, uidStr, False):
                    Utils.detectIsNoneButNoSave(config.universe_score, uidStr, '0/1')
                    Utils.detectIsNoneButNoSave(config.universe_fin, uidStr, False)
                    maxScore = str(config.universe_score[uidStr]).split('/')[1]
                    config.universe_score[uidStr] = f'0/{maxScore}'
                    config.universe_fin[uidStr] = False
                temp_text = f":活跃度:{Utils.getConfigValue(config.daily_tasks_score, uidStr)},模拟宇宙积分:{Utils.getConfigValue(config.universe_score, uidStr)}"
                options_reg.update({"<每日已完成>" + uidStr + temp_text
                                    if config.daily_tasks_fin[uidStr] 
                                    else 
                                    uidStr + temp_text: index})
            
            config.save_config()

            title_ = "请选择UID进行作为首位启动游戏:"
            firstTimeLogin = True
            option_ = questionary.select(title_, list(options_reg.keys())).ask()
            first_reg = options_reg.get(option_)

            for index in range(len(config.multi_login_accounts)):
                if firstTimeLogin:
                    index = first_reg
                    firstTimeLogin = False
                indexStr = config.multi_login_accounts[index]
                logger.info(_(indexStr))
                logger.debug(_("运行命令: cmd /C REG IMPORT {path}").format(path=indexStr))
                if os.system(f"cmd /C REG IMPORT {indexStr}"):
                    return False
                logger.info(action)
                run(index, action)
    else:
        logger.info(action)
        run(action)

def run(index=-1, action=None):
    # 完整运行
    if action is None or action == "main":
        logger.info(_("序列为{_index}的账号即将启动").format(_index= index))
        Version.start()
        Game.start()
        Daily.start()
        Game.stop(index ,True)
    # 子任务
    elif action in ["fight", "universe", "forgottenhall"]:
        Version.start()
        Game.start()
        if action == "fight":
            Fight.start()
        elif action == "universe":
            Universe.start(get_reward=True, nums=1, daily=False)
        elif action == "forgottenhall":
            ForgottenHall.start()
        Game.stop(index ,False)
    # 子任务 原生图形界面
    elif action in ["universe_gui", "fight_gui"]:
        if action == "universe_gui" and not Universe.gui():
            input(_("按回车键关闭窗口. . ."))
        elif action == "fight_gui" and not Fight.gui():
            input(_("按回车键关闭窗口. . ."))
        sys.exit(0)
    # 子任务 更新项目
    elif action in ["universe_update", "fight_update"]:
        if action == "universe_update":
            Universe.update()
        elif action == "fight_update":
            Fight.update()
        input(_("按回车键关闭窗口. . ."))
        sys.exit(0)
    elif action == "notify":
        from io import BytesIO
        from PIL import Image
        image_io = BytesIO()
        Image.open("./assets/app/images/March7th.jpg").save(image_io, format='JPEG')
        notify.notify(_("三月七小助手|･ω･)"), _("这是一条测试消息"),image_io)
        input(_("按回车键关闭窗口. . ."))
        sys.exit(0)
    else:
        logger.error(_("未知任务: {action}").format(action=action))
        input(_("按回车键关闭窗口. . ."))
        sys.exit(1)


def exit_handler():
    # 退出 OCR
    ocr.exit_ocr()


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logger.error(_("管理员权限获取失败"))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)
    else:
        try:
            atexit.register(exit_handler)
            main(sys.argv[1]) if len(sys.argv) > 1 else main()
        except KeyboardInterrupt:
            logger.error(_("发生错误: {e}").format(e=_("手动强制停止")))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)
        except Exception as e:
            logger.error(_("发生错误: {e}").format(e=e))
            notify.notify(_("发生错误: {e}").format(e=e))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)
