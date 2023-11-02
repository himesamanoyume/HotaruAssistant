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

loginDict = dict()
loginList = list()

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
 
            # notify.announcement(_("普罗丢瑟代练 - 公告"), _("我tm电脑炸了,脚本被迫停止,请大家暂时自行解决日常吧,1天内恢复的话会尽快重刷,1天以上恢复则补偿对应天数"))
            options_reg = dict()
            run_new_accounts()
            for index in range(len(config.multi_login_accounts)):
                uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
                account_active_fun(uidStr)
                if uidStr in config.blacklist_uid:
                    logger.warning(f"{uidStr}【正在黑名单中】")
                    continue
                if config.account_active[uidStr]['isExpired']:
                    logger.warning(f"{uidStr}【已过期】")
                    continue
                if not (config.account_active[uidStr]['ActiveDate'] <= config.account_active[uidStr]['ExpirationDate'] and config.account_active[uidStr]['ActiveDate'] != config.account_active[uidStr]['ExpirationDate']):
                    logger.error(f"{uidStr}【激活信息有异常】")
                    continue
                Utils.init_instanceButNoSave(uidStr)

                if Utils.is_next_4_am(config.last_run_timestamp, uidStr, False):
                    Utils.detectIsNoneButNoSave(config.daily_tasks_score, uidStr)
                    Utils.detectIsNoneButNoSave(config.daily_tasks_fin, uidStr, False)
                    config.account_active[uidStr]['ActiveDay'] -= 1
                    config.daily_tasks_score[uidStr] = 0
                    config.daily_tasks_fin[uidStr] = False
                    config.daily_tasks[uidStr] = {}

                if Utils.is_next_mon_4_am(config.universe_timestamp, uidStr, False):
                    Utils.detectIsNoneButNoSave(config.universe_score, uidStr, '0/1')
                    Utils.detectIsNoneButNoSave(config.universe_fin, uidStr, False)
                    maxScore = str(config.universe_score[uidStr]).split('/')[1]
                    config.universe_score[uidStr] = f'0/{maxScore}'
                    config.universe_fin[uidStr] = False
                
                loginDict.update({f'{uidStr}' : f'{str(config.multi_login_accounts[index])}'})
                loginList.append(f'{str(config.multi_login_accounts[index])}')
                temp_text = f":活跃度:{Utils.getConfigValue(config.daily_tasks_score, uidStr)},模拟宇宙积分:{Utils.getConfigValue(config.universe_score, uidStr)}"
                last_run_uidText = "【最后运行的账号】" if config.last_running_uid == uidStr else '' 
                options_reg.update({("<每日已完成>" + uidStr + temp_text + last_run_uidText
                                    if config.daily_tasks_fin[uidStr] 
                                    else 
                                    uidStr + temp_text + last_run_uidText)+ (f"【剩余{config.account_active[uidStr]['ActiveDay']}天】"): index})
            
            config.save_config()
            
            title_ = "请选择UID进行作为首位启动游戏:"
            option_ = questionary.select(title_, list(options_reg.keys())).ask()
            first_reg = options_reg.get(option_)

            firstTimeLogin = True
            jumpValue = ''
            jumpFin = False
            for value in loginList:
                if not firstTimeLogin and not jumpFin:
                    if not value == jumpValue:
                        continue
                    else:
                        jumpFin = True

                run_new_accounts()

                if firstTimeLogin:
                    firstTimeLogin = False
                    jumpValue = loginList[first_reg]
                    if jumpValue == value:
                        jumpFin = True
                    else:
                        continue

                logger.info(_(value))
                logger.debug(_("运行命令: cmd /C REG IMPORT {path}").format(path=value))
                if os.system(f"cmd /C REG IMPORT {value}"):
                    return False
                logger.info(action)
                run(index, action)
                
        input(_("按回车键关闭窗口. . ."))
        sys.exit(0)
    else:
        logger.info(action)
        run(action)

def run_new_accounts():
    logger.info("正在检测是否有新注册表加入")
    if len(config.want_register_accounts) > 1:
        logger.info("检测到有新注册表加入")
        for uid, item in config.want_register_accounts.items():
            if uid == '111111111': continue
            if item['reg_path']=='' or item['email']=='' or item['active_day'] == 0:
                logger.error(f"{uid}:新的注册信息未完整填写")
                input("按下回车跳过该次注册")
                return
            config.multi_login_accounts.append(item['reg_path'])
            loginList.append(f"{str(item['reg_path'])}")
            config.notify_smtp_To[uid] = item['email']
            config.account_active[uid] = {}
            config.account_active[uid]['isExpired'] = True
            config.account_active[uid]['isWantActive'] = True
            config.account_active[uid]['ActiveDate'] = 0
            config.account_active[uid]['ActiveDay'] = item['active_day']
            config.account_active[uid]['ExpirationDate'] = 0
            config.save_config()
            config.del_value('want_register_accounts', uid)
        logger.info("新注册表加入完成")
    else:
        logger.info("未检测到有新注册表加入")

        
def run(index=-1, action=None):
    # 完整运行
    if action is None or action == "main":
        # logger.info("run")
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
        # notify.notify(_("三月七小助手|･ω･)"), _("这是一条测试消息"),image_io)
        input(_("按回车键关闭窗口. . ."))
        sys.exit(0)
    else:
        logger.error(_("未知任务: {action}").format(action=action))
        input(_("按回车键关闭窗口. . ."))
        sys.exit(1)


def exit_handler():
    # 退出 OCR
    ocr.exit_ocr()

def account_active_fun(uid):
    # from datetime import datetime
    import time
    if config.account_active[uid]['isWantActive']:
        logger.info(f"{uid}:正在激活,新的激活天数为{config.account_active[uid]['ActiveDay']}天")
        if config.account_active[uid]['isExpired']:
            logger.info(f"{uid}:已过期用户正在重新激活")
            config.account_active[uid]['ActiveDate'] = time.time()
            config.account_active[uid]['isExpired'] = False

        config.account_active[uid]['ExpirationDate'] = config.account_active[uid]['ActiveDate'] + config.account_active[uid]['ActiveDay'] * 86400
        config.account_active[uid]['isWantActive'] = False   

    if config.account_active[uid]['ExpirationDate'] >= time.time() >= config.account_active[uid]['ExpirationDate'] - 3*86400:
        logger.warning(f"提醒:{uid}激活天数已不足3天")

    if config.account_active[uid]['ActiveDay'] >= 0 and config.account_active[uid]['ExpirationDate'] == 0 and config.account_active[uid]['ActiveDate']:
        logger.error(f"{uid}的激活信息异常")

    if time.time() >= config.account_active[uid]['ExpirationDate'] and config.account_active[uid]['ActiveDay'] == 0:
        logger.info(f"{uid}已过期,正在执行信息清除")
        config.account_active[uid]['isExpired'] = True
        config.account_active[uid]['ActiveDate'] = 0
        config.account_active[uid]['ActiveDay'] = 0
        config.account_active[uid]['ExpirationDate'] = 0
            
    config.save_config()


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
            # notify.notify(_("发生错误: {e}").format(e=e))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)