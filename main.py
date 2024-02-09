import os
import sys
os.chdir(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

from managers.notify_manager import notify
from managers.logger_manager import logger
from managers.config_manager import config
from managers.ocr_manager import ocr
from managers.translate_manager import _
from tasks.game.game import Game
from tasks.daily.daily import Daily
from tasks.daily.fight import Fight
from tasks.daily.utils import Utils
from datetime import datetime
from testFun import testFun
import questionary
from managers.automation_manager import auto
import time
from tasks.weekly.universe import Universe
from tasks.weekly.forgottenhall import ForgottenHall
import atexit
import pyuac
import glob
import shutil
from tasks.version.version import Version

loginDict = dict()
loginList = list()
lastUID = ''

def main(action=None):
    # 免责申明
    # if not config.agreed_to_disclaimer:
    #     logger.error(_("您尚未同意《免责声明》"))
    #     input(_("按回车键关闭窗口. . ."))
    #     sys.exit(0)
    config.reload()

    Version.start()
    Universe.check_path()
    
    if config.multi_login:
        # 多账号
        if len(config.multi_login_accounts) == 0:
            logger.warning("你并没有填写注册表位置")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            logger.info("开始多账号运行")

            options_reg = dict()
            run_new_accounts()

            config.reload()
            for index in range(len(config.multi_login_accounts)):
                uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]

            for index in range(len(config.multi_login_accounts)):
                uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
                if uidStr in config.blacklist_uid:
                    logger.warning(f"{uidStr}【正在黑名单中】")
                    continue

                Utils.init_instanceButNoSave(uidStr)

                # 分解遗器
                Utils.detectIsNoneButNoSave(config.relic_salvage_enable, uidStr, False)
                Utils.detectIsNoneButNoSave(config.relic_salvage_5star_enable, uidStr, False)

                # echo of war历战余响
                Utils.detectIsNoneButNoSave(config.echo_of_war_enable, uidStr, False)
                Utils.detectIsNoneButNoSave(config.echo_of_war_times, uidStr, 0)

                #daily每日
                Utils.detectIsNoneButNoSave(config.daily_tasks_score, uidStr, '0/1')
                Utils.detectIsNoneButNoSave(config.daily_tasks_fin, uidStr, False)
                

                # universe模拟宇宙
                Utils.detectIsNoneButNoSave(config.universe_fin, uidStr, False)
                Utils.detectIsNoneButNoSave(config.universe_number, uidStr, 3)
                Utils.detectIsNoneButNoSave(config.universe_difficulty, uidStr, 1)
                Utils.detectIsNoneButNoSave(config.universe_fate, uidStr, '巡猎')
                Utils.detectIsNoneButNoSave(config.universe_team, uidStr, {})
                Utils.detectIsNoneButNoSave(config.universe_score, uidStr, '0/1')
                Utils.detectIsNoneButNoSave(config.universe_fin, uidStr, False)

                if Utils.is_next_4_am(config.last_run_timestamp, uidStr, False):
                    config.daily_tasks_score[uidStr] = 0
                    config.daily_tasks_fin[uidStr] = False
                    config.daily_tasks[uidStr] = {}
                

                if Utils.is_next_mon_4_am(config.universe_timestamp, uidStr, False):
                    maxScore = str(config.universe_score[uidStr]).split('/')[1]
                    config.universe_score[uidStr] = f'0/{maxScore}'
                    config.universe_fin[uidStr] = False

                config.save_config()
                
                config.reload()
                loginDict.update({f'{uidStr}' : f'{str(config.multi_login_accounts[index])}'})
                loginList.append(f'{str(config.multi_login_accounts[index])}')
                temp_text = f":活跃度:{Utils.getConfigValue(config.daily_tasks_score, uidStr)},模拟宇宙积分:{Utils.getConfigValue(config.universe_score, uidStr)}"
                last_run_uidText = "【最后运行的账号】" if config.last_running_uid == uidStr else '' 
                options_reg.update({("<每日已完成>" + uidStr + temp_text + last_run_uidText
                                    if config.daily_tasks_fin[uidStr] 
                                    else 
                                    uidStr + temp_text + last_run_uidText) : index})
            
            config.save_config()

            title_ = "请选择UID进行作为首位启动游戏:"
            option_ = questionary.select(title_, list(options_reg.keys())).ask()
            first_reg = options_reg.get(option_)

            isFirstTimeLoop = True

            while True:
                config.reload()
                logger.info(f"config已重载")
                if not os.path.exists("./backup"):
                    os.makedirs("./backup")
                shutil.copy("./config.yaml",f"./backup/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.config.yaml")

                lastUID = str(loginList[len(loginList) - 1]).split('-')[1][:9]
                logger.info(f"当前列表最后一个账号UID为:{lastUID}")
                Utils._loop_start_timestamp = time.time()

                firstTimeLogin = True
                jumpValue = ''
                jumpFin = False
                # 若只启动模拟宇宙,该循环就只有1次,只进行模拟宇宙
                if action == "universe":
                    count = 1
                else:
                    count = 2
                for turn in range(count):
                    config.reload()
                    for value in loginList:
                        if not firstTimeLogin and not jumpFin:
                            if not value == jumpValue:
                                continue
                            else:
                                jumpFin = True

                        uidStr2 = str(value).split('-')[1][:9]
                        run_new_accounts()

                        if isFirstTimeLoop:
                            if firstTimeLogin:
                                firstTimeLogin = False
                                jumpValue = loginList[first_reg]
                                if jumpValue == value:
                                    jumpFin = True
                                else:
                                    continue

                        logger.info(f"运行命令: cmd /C REG IMPORT {value}")

                        if os.system(f"cmd /C REG IMPORT {value}"):
                            input("导入注册表出错,检查对应注册表路径和配置是否正确,按回车键退出...")
                            return False
                            
                        # logger.info(action)
                        if count == 1:
                            run(index, "universe", uidStr2, lastUID)
                        else:
                            if turn == 0:
                                run(index, None, uidStr2, lastUID)
                            else:
                                run(index, "universe", uidStr2, lastUID)
                        isFirstTimeLoop = False
        # input(_("按回车键关闭窗口. . ."))
        # sys.exit(0)
    else:
        logger.info(action)
        run(action)

def run_new_accounts():
    logger.info("正在检测是否有新注册表加入")
    config.reload()
    if len(config.want_register_accounts) > 1:
        logger.info("检测到有新注册表加入")
        for uid, item in config.want_register_accounts.items():
            if uid == '111111111': continue
            if item['reg_path']=='':
                logger.error(f"{uid}:新的注册信息中注册表地址未完整填写")
                input("按下回车跳过该次注册")
                return
            if item['email']=='':
                logger.error(f"{uid}:新的注册信息中邮箱未完整填写")
                input("按下回车跳过该次注册")
                return
            if not len(item['universe_team']) == 4:
                logger.error(f"{uid}:新的注册信息中模拟宇宙小队角色未填写满4人或超出4人")
                input("按下回车跳过该次注册")
                return
            if not item['universe_fate'] in ['存护','记忆','虚无','丰饶','巡猎','毁灭','欢愉','繁育']:
                logger.error(f"{uid}:新的注册信息中模拟宇宙命途不合法")
                input("按下回车跳过该次注册")
                return
            if not item['universe_number'] in [3,4,5,6,7]:
                logger.error(f"{uid}:新的注册信息中模拟宇宙选择的世界不合法")
                input("按下回车跳过该次注册")
                return
            if not item['universe_difficulty'] in [1,2,3,4,5]:
                logger.error(f"{uid}:新的注册信息中模拟宇宙难度不合法")
                input("按下回车跳过该次注册")
                return
            config.reload()
            config.multi_login_accounts.append(item['reg_path'])
            loginList.append(f"{str(item['reg_path'])}")
            config.notify_smtp_To[uid] = item['email']

            config.universe_number[uid] = item['universe_number']
            config.universe_difficulty[uid] = item['universe_difficulty']
            config.universe_fate[uid] = item['universe_fate']
            config.universe_team[uid] = item['universe_team']

            config.save_config()
            config.del_value('want_register_accounts', uid)
        logger.info("新注册表加入完成")
    else:
        logger.info("未检测到有新注册表加入")

def run(index=-1, action=None, currentUID=0, _lastUID=-1):
    # 完整运行
    if action is None or action == "main":
        # logger.info("run")
        # Version.start()
        try:
            logger.info("本次为每日流程")
            Utils._action = '每日任务流程'
            Game.start()
            Daily.start()
            Game.stop(index ,True, currentUID, _lastUID, action=action)
            Utils._action = ''
        except Exception as e:
            
            logger.error(f"{e}")
            notify.announcement((f'运行流程异常|{Utils._action}'), (f"<p>本次运行已中断</p><p>时间戳:{e}</p>"), isSingle=True)
            logger.error("进入非正常退出游戏流程")
            auto.press_key(']')
            time.sleep(2)
            files = glob.glob('./records/*')
            for f in files:
                if os.path.isfile(f):
                    os.remove(f)
            Game.stop(index ,True, currentUID, _lastUID, isAbnormalExit=True)
            Utils._action = ''
        
    # 子任务
    elif action in ["fight", "universe", "forgottenhall"]:
        # Version.start()
        try:
            if action == "universe":
                logger.info("本次为模拟宇宙专属")
                Utils._action = '模拟宇宙流程'
            Game.start()
            if action == "fight":
                Fight.start()
            elif action == "universe":
                Daily.start_ready()
                if config.instance_type[currentUID] == '模拟宇宙' or not config.universe_fin[currentUID]:
                    Universe.start(get_reward=True, daily=True, nums=0)
                else:
                    logger.info("因为未选择清模拟宇宙,跳过")
                Daily.end()
            elif action == "forgottenhall":
                ForgottenHall.start()

            if config.instance_type[currentUID] == '模拟宇宙' or (not config.universe_fin[currentUID] or Utils._totalTime >= 900):
                Game.stop(index ,True, currentUID, _lastUID, action=action)
            else:
                logger.info("因为未选择清模拟宇宙或模拟宇宙已通关,不发送邮件通知号主")
                Game.stop(index ,True, currentUID, _lastUID, action=action, isSendEmail=False)
                Utils._action = ''
        except Exception as e:
            logger.error(f"{e}")
            notify.announcement((f'运行流程异常|{Utils._action}'), (f"<p>本次运行已中断</p><p>时间戳:{e}</p>"), isSingle=True)
            logger.error("进入非正常退出游戏流程")
            auto.press_key(']')
            time.sleep(2)
            files = glob.glob('./records/*')
            for f in files:
                if os.path.isfile(f):
                    os.remove(f)
            Game.stop(index ,True, currentUID, _lastUID, isAbnormalExit=True)
            Utils._action = ''
    else:
        logger.error(f"未知任务: {action}")
        input("按回车键关闭窗口. . .")
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
            logger.error("管理员权限获取失败")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    else:
        try:
            atexit.register(exit_handler)
            main(sys.argv[1]) if len(sys.argv) > 1 else main()
        except KeyboardInterrupt:
            logger.error("发生错误: 手动强制停止")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        except Exception as e:
            logger.error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
            sys.exit(0)