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

def temp_fun():
    from managers.automation_manager import auto
    import time

    # countdownTextCrop=(1478.0 / 1920, 318.0 / 1080, 166.0 / 1920, 42.0 / 1080)
    # countdownText = auto.get_single_line_text(crop=countdownTextCrop, blacklist=[], max_retries=7)
    # countdownText = countdownText.replace('）','')
    # logger.info(countdownText)
    input(_("按回车键开始. . ."))
    # return

    crop1=(534.0 / 1920, 373.0 / 1080, 845.0 / 1920, 267.0 / 1080) # 成功奖励下的遗器布局
    # crop2=(526.0 / 1920, 628.0 / 1080, 133.0 / 1920, 33.0 / 1080) # 遗器星级数
    crop3=(783.0 / 1920, 318.0 / 1080, 436.0 / 1920, 53.0 / 1080) # 遗器名称
    crop4=(831.0 / 1920, 398.0 / 1080, 651.0 / 1920, 181.0 / 1080) # 遗器属性2

    crop9=(239.0 / 1920, 445.0 / 1080, 133.0 / 1920, 151.0 / 1080) # 宇宙第一行第一格 x=180
    crop10=(424.0 / 1920, 445.0 / 1080, 133.0 / 1920, 151.0 / 1080) # 宇宙第一行第2格
    crop11=(604.0 / 1920, 445.0 / 1080, 133.0 / 1920, 151.0 / 1080)  # 宇宙第一行第3格


    # crop5=(545.0 / 1920, 381.0 / 1080, 114.0 / 1920, 119.0 / 1080) # 一行第一格
    # crop5_1=(664.0 / 1920, 505.0 / 1080, 0.0 / 1920, 0.0 / 1080) # 一行第一格大
    # crop6=(665.0 / 1920, 381.0 / 1080, 114.0 / 1920, 119.0 / 1080) # 一行第二格
    # crop7=(1265.0 / 1920, 381.0 / 1080, 114.0 / 1920, 119.0 / 1080) # 一行第七格,最后一格 x=120距离
    # crop8=(545.0 / 1920, 504.0 / 1080, 114.0 / 1920, 119.0 / 1080) # 二行第一格

    relic_name_crop=(783.0 / 1920, 318.0 / 1080, 436.0 / 1920, 53.0 / 1080) # 遗器名称
    relic_prop_crop=(831.0 / 1920, 398.0 / 1080, 651.0 / 1920, 181.0 / 1080) # 遗器属性
    crop=(538.0 / 1920, 427.0 / 1080, 124.0 / 1920, 122.0 / 1080)
    logger.info("开始检测遗器")

    # top left,   bottom right
    # ((915, 388), (1002, 414))
    point = auto.find_element("./assets/images/fight/fight_reward.png", "image", 0.9, max_retries=2)
    success_reward_top_left_x = point[0][0]
    success_reward_top_left_y = point[0][1]
    # auto.click_element_with_pos(((915-380, 388+40), (915-380+144, 388+40+119)))
    # auto.click_element("./assets/images/fight/relic.png", "image", 0.9, max_retries=2, crop=((success_reward_top_left_x - 380)/ 1920, (success_reward_top_left_y + 40) / 1080, 120.0 / 1920, 120.0 / 1080))

    # return

    for i in range(2):
        for j in range(7):
            
            if auto.click_element("./assets/images/fight/relic.png", "image", 0.9, max_retries=2, crop=((success_reward_top_left_x - 380 + j*120.0 )/ 1920, (success_reward_top_left_y + 40 + i*120) / 1080, 120.0 / 1920, 120.0 / 1080)):
                time.sleep(0.5)

                relic_name = auto.get_single_line_text(relic_name_crop, blacklist=[], max_retries=5)
                logger.info(relic_name)
                
                auto.take_screenshot(crop=relic_prop_crop)
                time.sleep(0.5)
                result = ocr.recognize_multi_lines(auto.screenshot)

                isProp = False
                tempPropName = ''
                tempMainPropName = ''
                tempPropValue = ''
                propCount = -1
                usefulPropCount = 0
                relicDict = dict()
                isMainProp = True

                for box in result:
                    text = box[1][0]
                    if text in ['暴击率','暴击伤害','生命值','攻击力','防御力','能量恢复效率','效果命中','效果抵抗','速度','击破特攻','治疗量加成','量子属性伤害加成','风属性伤害加成','火属性伤害加成','雷属性伤害加成','冰属性伤害加成','虚数属性伤害加成']:
                        if isMainProp:
                            tempMainPropName = text
                        tempPropName = text
                        isProp = True
                        if text in ['暴击率','暴击伤害']:
                            usefulPropCount += 1
                        continue
                    elif isProp:
                        if isMainProp:
                            isMainProp = False

                        tempPropValue = text
                        isProp = False
                        propCount += 1
                    else:
                        continue

                    logger.info(f"{tempPropName}:{tempPropValue}")
                    relicDict.update({tempPropName:tempPropValue})
                if (propCount == 3 and usefulPropCount >= 1) or (propCount == 4 and usefulPropCount == 2) or (tempMainPropName in ['暴击率','暴击伤害','速度','量子属性伤害加成','风属性伤害加成','火属性伤害加成','雷属性伤害加成','冰属性伤害加成','虚数属性伤害加成','能量恢复效率'] and propCount == 3 and usefulPropCount>=1):
                    logger.info(f"发现胚子")
                    Utils._content['relic_content'] += f"<div class=relic><p><strong>{relic_name}</strong></p>"
                    isMain = True
                    for propName, propValue in relicDict.items():
                        if isMain:
                            Utils._content['relic_content'] += f"<div class=relicPropContainer><p><span class=important>{propName}:{propValue}</span></p>"
                            isMain = False
                        else:
                            Utils._content['relic_content'] += f"<p>{propName}:{propValue}</p>"

                    Utils._content['relic_content'] += "</div></div>"
                    if auto.click_element("./assets/images/fight/relic_lock.png", "image", 0.9, max_retries=3):
                        time.sleep(1)

                
                time.sleep(0.5)
                if auto.click_element("./assets/images/fight/relic_info_close.png", "image", 0.9, max_retries=3):
                    time.sleep(0.5)


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
            
            # temp_fun()
            # input(_("按回车键关闭窗口. . ."))
            # return
            # notify.announcement(_("普罗丢瑟代练 - 公告"), _("<p>我tm电脑炸了,脚本被迫停止,请大家暂时自行解决日常吧,1天内恢复的话会尽快重刷,1天以上恢复则补偿对应天数</p>"))
            # input(_("按回车键关闭窗口. . ."))
            # sys.exit(0)

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

                uidStr2 = str(value).split('-')[1][:9]
                run_new_accounts()
                account_active_fun(uidStr2)

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

    if config.account_active[uid]['ActiveDay'] >= 0:
        temp = int((config.account_active[uid]['ExpirationDate'] - time.time()) // 86400)
        if temp < 0:
            config.account_active[uid]['ActiveDay'] = 0
        else:
            config.account_active[uid]['ActiveDay'] = temp
    elif config.account_active[uid]['ActiveDay'] < 0:
        config.account_active[uid]['ActiveDay'] = 0

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