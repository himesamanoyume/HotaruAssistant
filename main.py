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

loginDict = dict()
loginList = list()
lastUID = ''

def main(action=None):
    # 免责申明
    # if not config.agreed_to_disclaimer:
    #     logger.error(_("您尚未同意《免责声明》"))
    #     input(_("按回车键关闭窗口. . ."))
    #     sys.exit(0)
    if config.multi_login:
        # 多账号
        if len(config.multi_login_accounts) == 0:
            logger.warning("你并没有填写注册表位置")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
        else:
            logger.info("开始多账号运行")
            # input(_("按回车键关闭窗口. . ."))
            # testFun()
            # input(_("按回车键关闭窗口. . ."))
            # return

            options_reg = dict()
            run_new_accounts()
            modify_all_account_active_day()

            # notify.announcement(_("HimeProducer - 公告"), _("我tm电脑炸了,脚本被迫停止,请大家暂时自行解决日常吧,1天内恢复的话会尽快重刷,1天以上恢复则补偿对应天数"))
            # notify.announcement("某UID运行时长超时警告!", "有某UID玩家运行时长超40分钟!这得治!", isSingle=True)
            # input(_("按回车键关闭窗口. . ."))
            # sys.exit(0)
            for index in range(len(config.multi_login_accounts)):
                uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
                account_active_fun(uidStr)

            for index in range(len(config.multi_login_accounts)):
                uidStr = str(config.multi_login_accounts[index]).split('-')[1][:9]
                # account_active_fun(uidStr)
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

                # 分解遗器
                Utils.detectIsNoneButNoSave(config.relic_salvage_enable, uidStr, False)

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
                
                loginDict.update({f'{uidStr}' : f'{str(config.multi_login_accounts[index])}'})
                loginList.append(f'{str(config.multi_login_accounts[index])}')
                temp_text = f":活跃度:{Utils.getConfigValue(config.daily_tasks_score, uidStr)},模拟宇宙积分:{Utils.getConfigValue(config.universe_score, uidStr)}"
                last_run_uidText = "【最后运行的账号】" if config.last_running_uid == uidStr else '' 
                options_reg.update({("<每日已完成>" + uidStr + temp_text + last_run_uidText
                                    if config.daily_tasks_fin[uidStr] 
                                    else 
                                    uidStr + temp_text + last_run_uidText)+ (f"【剩余{round((config.account_active[uidStr]['ActiveDay'] - config.account_active[uidStr]['CostDay']), 3)}天】"): index})
            
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
                        modify_all_account_active_day()
                        account_active_fun(uidStr2)

                        if isFirstTimeLoop:
                            if firstTimeLogin:
                                firstTimeLogin = False
                                jumpValue = loginList[first_reg]
                                if jumpValue == value:
                                    jumpFin = True
                                else:
                                    continue

                        logger.info(value)
                        logger.debug("运行命令: cmd /C REG IMPORT {path}".format(path=value))
                    
                        if os.system(f"cmd /C REG IMPORT {value}"):
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
            if item['active_day'] == 0:
                logger.error(f"{uid}:新的注册信息中激活天数未填写")
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
            config.account_active[uid] = {}
            config.account_active[uid]['isExpired'] = True
            config.account_active[uid]['isWantActive'] = True
            config.account_active[uid]['ActiveDate'] = 0
            config.account_active[uid]['ActiveDay'] = item['active_day']
            config.account_active[uid]['ExpirationDate'] = 0
            config.account_active[uid]['CostDay'] = 0

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
                Game.stop(index ,True, currentUID, _lastUID, action=action, isSendEmail=False)
                Utils._action = ''
                logger.info("因为未选择清模拟宇宙或模拟宇宙已通关,不发送邮件通知号主")
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
        logger.error(f"未知任务: {action}")
        input("按回车键关闭窗口. . .")
        sys.exit(1)

def exit_handler():
    # 退出 OCR
    ocr.exit_ocr()

def modify_all_account_active_day():
    if config.all_account_active_day > 0:
        for index in range(len(config.multi_login_accounts)):
            uidStr3 = str(config.multi_login_accounts[index]).split('-')[1][:9]
            if not config.account_active[uidStr3]['isExpired']:
                config.account_active[uidStr3]['isWantActive'] = True
                config.account_active[uidStr3]['ActiveDay'] += config.all_account_active_day
        config.save_config()
        logger.info(f"为所有未过期账号延长{config.all_account_active_day}天时间")
        notify.announcement(_("普罗丢瑟代练 - 通知"), _(f"<p>为所有未过期账号延长{config.all_account_active_day}天时间</p>"))
        config.set_value('all_account_active_day', 0)
    elif config.all_account_active_day == 0:
        return
    else:
        logger.error(f"延长账号时间不合法,已取消")
        config.set_value('all_account_active_day', 0)

def account_active_fun(uid):
    if config.account_active[uid]['isWantActive']:
        logger.info(f"{uid}:正在激活,新的激活天数为{config.account_active[uid]['ActiveDay']}天")
        if config.account_active[uid]['isExpired']:
            logger.info(f"{uid}:已过期用户正在重新激活")
            config.account_active[uid]['ActiveDate'] = time.time()
            config.account_active[uid]['CostDay'] = 0
            config.account_active[uid]['isExpired'] = False

        config.account_active[uid]['ExpirationDate'] = (config.account_active[uid]['ActiveDate'] + (config.account_active[uid]['ActiveDay'] * 86400))
        config.account_active[uid]['isWantActive'] = False 

    if config.account_active[uid]['ActiveDay'] >= 0 and not config.account_active[uid]['isExpired']:
        costDay = (time.time() - config.account_active[uid]['ActiveDate']) / 86400
        if costDay > 0:
            config.account_active[uid]['CostDay'] = round(costDay, 3)
        else:
            config.account_active[uid]['CostDay'] = 0

    elif config.account_active[uid]['ActiveDay'] < 0:
        logger.error(f"{uid}激活时间不合法,已设为0")
        config.account_active[uid]['ActiveDay'] = 0

    if config.account_active[uid]['ExpirationDate'] >= time.time() >= config.account_active[uid]['ExpirationDate'] - 3*86400:
        logger.warning(f"提醒:{uid}激活天数已不足3天")

    if config.account_active[uid]['ActiveDay'] >= 0 and config.account_active[uid]['ExpirationDate'] == 0 and config.account_active[uid]['ActiveDate']:
        logger.error(f"{uid}的激活信息异常")

    if time.time() >= config.account_active[uid]['ExpirationDate'] and (config.account_active[uid]['CostDay'] >= config.account_active[uid]['ActiveDay']) and (not config.account_active[uid]['isExpired']):
        logger.info(f"{uid}已过期,正在执行信息清除")
        config.account_active[uid]['isExpired'] = True
        config.account_active[uid]['ActiveDate'] = 0
        config.account_active[uid]['ActiveDay'] = 0
        # config.account_active[uid]['ExpirationDate'] = 0
        config.account_active[uid]['CostDay'] = 0

    if time.time() >= config.account_active[uid]['ExpirationDate'] and config.account_active[uid]['isExpired']:
        costDay = (time.time() - config.account_active[uid]['ExpirationDate']) / 86400
        if costDay > 0:
            config.account_active[uid]['CostDay'] = round(costDay, 3)
        else:
            config.account_active[uid]['CostDay'] = 0

        if config.account_active[uid]['CostDay'] >= 15:
            logger.info(f"{uid}已过期15天,正在执行配置清除")
            try:
                config.del_value_with_no_save('instance_type',uid)
                config.del_value_with_no_save('instance_names',uid)
                config.del_value_with_no_save('echo_of_war_enable',uid)
                config.del_value_with_no_save('echo_of_war_timestamp',uid)
                config.del_value_with_no_save('echo_of_war_times',uid)
                config.del_value_with_no_save('relic_salvage_enable',uid)
                config.del_value_with_no_save('daily_tasks',uid)
                config.del_value_with_no_save('daily_tasks_score',uid)
                config.del_value_with_no_save('daily_tasks_fin',uid)
                config.del_value_with_no_save('last_run_timestamp',uid)
                config.del_value_with_no_save('fight_timestamp',uid)
                config.del_value_with_no_save('universe_fin',uid)
                config.del_value_with_no_save('universe_score',uid)
                config.del_value_with_no_save('universe_timestamp',uid)
                config.del_value_with_no_save('universe_number',uid)
                config.del_value_with_no_save('universe_difficulty',uid)
                config.del_value_with_no_save('universe_fate',uid)
                config.del_value_with_no_save('universe_team',uid)
                config.del_value_with_no_save('forgottenhall_stars',uid)
                config.del_value_with_no_save('forgottenhall_levels',uid)
                config.del_value_with_no_save('forgottenhall_timestamp',uid)
                config.del_value_with_no_save('notify_smtp_To',uid)
                config.del_value_with_no_save('account_active',uid)

                for index in range(len(config.multi_login_accounts)):
                    if uid in config.multi_login_accounts[index]:
                        config.del_value_with_no_save('multi_login_accounts', index)

                for index in range(len(config.blacklist_uid)):
                    if uid in config.blacklist_uid[index]:
                        config.del_value_with_no_save('blacklist_uid', index)
                
                if uid in loginList:
                    loginList.remove(uid)

                if uid in loginDict:
                    loginDict.pop(uid)

            except Exception as e:
                logger.warning(e)
                input('...')
                sys.exit(0)
            
    config.save_config()

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