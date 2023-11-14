from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.config_manager import config
from managers.logger_manager import logger
from managers.translate_manager import _
from tasks.daily.utils import Utils
from module.automation.screenshot import Screenshot
from tasks.base.base import Base
import time


class ForgottenHall:
    @staticmethod
    def wait_fight(count, boss_count, max_recursion):
        logger.info(_("进入战斗"))
        for i in range(20):
            if auto.find_element("./assets/images/base/2x_speed_off.png", "image", 0.95, crop=(1630.0 / 1920, 24.0 / 1080, 60.0 / 1920, 45.0 / 1080)):
                logger.info(_("尝试开启二倍速"))
                auto.press_key("b")
            elif auto.find_element("./assets/images/base/2x_speed_on.png", "image", 0.95, crop=(1630.0 / 1920, 24.0 / 1080, 60.0 / 1920, 45.0 / 1080)):
                logger.info(_("二倍速已开启"))
                break
            time.sleep(0.5)
        for i in range(20):
            if auto.find_element("./assets/images/base/not_auto.png", "image", 0.95):
                logger.info(_("尝试开启自动战斗"))
                auto.press_key("v")
            elif auto.find_element("./assets/images/base/auto.png", "image", 0.95, take_screenshot=False):
                logger.info(_("自动战斗已开启"))
                break
            time.sleep(0.5)
        logger.info(_("等待战斗"))

        def check_fight():
            if auto.find_element("./assets/images/forgottenhall/prepare_fight.png", "image", 0.9, crop=(64 / 1920, 277 / 1080, 167 / 1920, 38 / 1080)):
                # 正常
                return 1
            elif auto.find_element("./assets/images/forgottenhall/back.png", "image", 0.9, crop=(560 / 1920, 900 / 1080, 796 / 1920, 76 / 1080)):
                logger.info(_("战斗完成"))
                # 挑战失败
                result = auto.find_element("./assets/images/forgottenhall/again.png", "image", 0.9,
                                           max_retries=2, crop=(560 / 1920, 900 / 1080, 796 / 1920, 76 / 1080))
                if result and max_recursion > 0:
                    # 重新挑战
                    logger.info(_("重新挑战"))
                    auto.click_element("./assets/images/forgottenhall/again.png", "image", 0.9,
                                       max_retries=10, crop=(560 / 1920, 900 / 1080, 796 / 1920, 76 / 1080))
                    auto.click_element("./assets/images/forgottenhall/start.png", "image", 0.8,
                                       max_retries=10, crop=(1546 / 1920, 962 / 1080, 343 / 1920, 62 / 1080))
                    ForgottenHall.click_message_box()
                    # 重新挑战整间
                    if ForgottenHall.start_fight(count, boss_count, max_recursion - 1):
                        return 4  # 挑战失败，重试后成功
                    return 3  # 挑战失败，重试后失败
                else:
                    auto.click_element("./assets/images/forgottenhall/back.png", "image", 0.9,
                                       max_retries=2, crop=(560 / 1920, 900 / 1080, 796 / 1920, 76 / 1080))
                    # 等待返回关卡选择界面
                    if result:
                        return 3  # 挑战失败，无重试次数
                    return 2  # 挑战成功
            return False
        result = auto.retry_with_timeout(lambda: check_fight(), 30 * 60, 1)
        if not result:
            nowtime = time.time()
            logger.error(_(f"{nowtime},战斗超时"))
            raise Exception(_(f"{nowtime},战斗超时"))
        return result

    @staticmethod
    def start_fight(count, boss_count, max_recursion=config.forgottenhall_retries, team=None):
        logger.debug(_("剩余重试次数:{max_recursion}".format(max_recursion=max_recursion)))
        for i in range(count):
            logger.info(_("进入第{i}间").format(i=i + 1))
            auto.press_key("w", 3.5)

            # 释放秘技
            if team:
                last_index = None
                for index, character in enumerate(team):
                    if character[1] > 0:
                        auto.press_key(f"{index+1}")
                        time.sleep(1)
                        for i in range(character[1]):
                            auto.press_key(config.get_value("hotkey_technique"))
                            time.sleep(1)
                    elif character[1] == -1:
                        last_index = index
            else:
                last_index = None
                for index, character in enumerate(config.get_value("forgottenhall_team" + str(i + 1))):
                    if character[1] > 0:
                        auto.press_key(f"{index+1}")
                        time.sleep(1)
                        for i in range(character[1]):
                            auto.press_key(config.get_value("hotkey_technique"))
                            time.sleep(1)
                    elif character[1] == -1:
                        last_index = index
            # 设置了末位角色
            if last_index is not None:
                auto.press_key(f"{last_index+1}")
                time.sleep(1)

            for i in range(boss_count):
                logger.info(_("挑战第{i}个boss").format(i=i + 1))

                # 适配近战角色开怪
                if boss_count == 2:
                    if i == 0:
                        auto.press_key("a", 1)
                    elif i == 1:
                        auto.press_key("d", 2)

                # 开怪
                auto.press_key(config.get_value("hotkey_technique"))
                for i in range(3):
                    auto.press_mouse()

                result = ForgottenHall.wait_fight(count, boss_count, max_recursion)

                if result == 3:
                    return False
                elif result == 4:
                    return True
            time.sleep(1)
        return True

    @staticmethod
    def click_message_box():
        if auto.find_element("剩余", "text", max_retries=20, crop=(64 / 1920, 277 / 1080, 167 / 1920, 38 / 1080), include=True):
            time.sleep(1)
            auto.press_key("esc")
            time.sleep(1)

    @staticmethod
    def select_characters(team_config, team_image_path):
        if auto.click_element(team_image_path, "image", 0.8, max_retries=10, crop=(610 / 1920, 670 / 1080, 118 / 1920, 218 / 1080)):
            auto.take_screenshot(crop=(30 / 1920, 115 / 1080, 530 / 1920, 810 / 1080))
            for character in team_config:
                if not auto.click_element(f"./assets/images/character/{character[0]}.png", "image", 0.8, max_retries=10, take_screenshot=False):
                    return False
                time.sleep(1)
            return True
        return False

    @staticmethod
    def configure_teams():
        if auto.find_element("./assets/images/forgottenhall/team1.png", "image", 0.8, max_retries=10, crop=(610 / 1920, 670 / 1080, 118 / 1920, 218 / 1080)):
            if ForgottenHall.select_characters(config.forgottenhall_team1, "./assets/images/forgottenhall/team1.png"):
                if ForgottenHall.select_characters(config.forgottenhall_team2, "./assets/images/forgottenhall/team2.png"):
                    if auto.click_element("./assets/images/forgottenhall/start.png", "image", 0.8, max_retries=10, crop=(1546 / 1920, 962 / 1080, 343 / 1920, 62 / 1080)):
                        return True
        return False

    @staticmethod
    def change_to(number, max_retries=4):
        # crop = (0, 0, 1, 900 / 1080)
        crop = (112 / 1920, 252 / 1080, 1700 / 1920, 650 / 1080)
        window = Screenshot.get_window(config.game_title_name)
        left, top, width, height = Screenshot.get_window_region(window)

        for i in range(max_retries):
            result = auto.find_element(number, "text", max_retries=4, crop=crop, relative=True)
            if result:
                return (result[0][0] + width * crop[0], result[0][1] + height * crop[1])

            # 先向右滚动4次查找，然后向左
            for direction in [-1, 1]:
                for i in range(4):
                    auto.mouse_scroll(3, direction)
                    time.sleep(3)

                    result = auto.find_element(number, "text", max_retries=1, crop=crop, relative=True)
                    if result:
                        return (result[0][0] + width * crop[0], result[0][1] + height * crop[1])

                    if (direction == -1 and auto.find_element("10", "text", need_ocr=False)) or \
                            (direction == 1 and auto.find_element("01", "text", need_ocr=False)):
                        break

        return False

    @staticmethod
    def check_star(top_left):
        window = Screenshot.get_window(config.game_title_name)
        left, top, width, height = Screenshot.get_window_region(window)
        crop = (top_left[0] / width, top_left[1] / height, 120 / 1920, 120 / 1080)
        count = auto.find_element("./assets/images/forgottenhall/star.png", "image_count", 0.6, crop=crop, pixel_bgr=[112, 200, 255])
        return count if count is not None and 0 <= count <= 3 else None

    @staticmethod
    def run():
        # 记录层数
        max_level = 0
        auto.mouse_scroll(20, 1)
        time.sleep(1)
        for i in range(config.forgottenhall_level[0], config.forgottenhall_level[1] + 1):
            # 选择关卡
            top_left = ForgottenHall.change_to(f"{i:02}")
            if not top_left:
                logger.error(_("切换关卡失败"))
                break
            logger.debug(_("选择关卡:{top_left}").format(top_left=top_left))
            # 判断星数
            star_count = ForgottenHall.check_star(top_left)
            if star_count == 3:
                logger.info(_("第{i}层已满星").format(i=f"{i:02}"))
                continue
            else:
                logger.info(_("第{i}层星数{star_count}").format(i=i, star_count=star_count))
                auto.click_element(f"{i:02}", "text", max_retries=20, crop=(0, 336 / 1080, 1, 537 / 1080))

            logger.info(_("开始挑战第{i}层").format(i=f"{i:02}"))
            # 选择角色
            if not ForgottenHall.configure_teams():
                logger.error(_("配置队伍失败，请检查是否在设置中配置好两个队伍！！！"))
                break

            # 点击弹出框
            ForgottenHall.click_message_box()
            # 判断关卡BOSS数量
            boss_count = 2 if i in range(1, 6) else 1
            if not ForgottenHall.start_fight(2, boss_count):
                logger.info(_("挑战失败"))
            else:
                logger.info(_("挑战成功"))
                max_level = i

            # 进入混沌回忆关卡选择界面
            time.sleep(2)
            if not auto.find_element("./assets/images/screen/forgottenhall/memory_of_chaos.png", "image", 0.8, max_retries=10, crop=(36 / 1920, 25 / 1080, 170 / 1920, 80 / 1080)):
                # if not auto.find_element("混沌回忆", "text", max_retries=10):
                logger.error(_("界面不正确，尝试切换到混沌回忆界面"))
                screen.change_to('memory_of_chaos')

        if max_level > 0:
            screen.change_to('memory_of_chaos')
            # 领取星琼
            if auto.click_element("./assets/images/dispatch/reward.png", "image", 0.9, crop=(1775.0 / 1920, 902.0 / 1080, 116.0 / 1920, 110.0 / 1080)):
                time.sleep(1)
                while auto.click_element("./assets/images/forgottenhall/receive.png", "image", 0.9, crop=(1081.0 / 1920, 171.0 / 1080, 500.0 / 1920, 736.0 / 1080)):
                    auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10)
                    time.sleep(1)
            logger.info("🎉混沌回忆已通关{max_level}层🎉").format(max_level=max_level)
            # Base.send_notification_with_screenshot(_("🎉混沌回忆已通关{max_level}层🎉").format(max_level=max_level))
            auto.press_key("esc")
            time.sleep(1)

    @staticmethod
    def prepare():
        flag = False
        screen.change_to('guide3')
        guide3_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        if auto.click_element("侵蚀隧洞", "text", max_retries=10, crop=guide3_crop):
            auto.mouse_scroll(12, -1)
            if auto.click_element("忘却之庭", "text", max_retries=10, crop=guide3_crop):
                auto.find_element("混沌回忆", "text", max_retries=10, crop=(689.0 / 1920, 285.0 / 1080, 970.0 / 1920, 474.0 / 1080), include=True)
                for box in auto.ocr_result:
                    text = box[1][0]
                    if "/30" in text:
                        logger.info(_("星数：{text}").format(text=text))
                        if text.split("/")[0] == "30":
                            logger.info(_("混沌回忆未刷新"))
                            screen.change_to('menu')
                            return True
                        else:
                            break
                if auto.click_element("传送", "text", max_retries=10, need_ocr=False):
                    auto.click_element("./assets/images/forgottenhall/memory_of_chaos.png", "image",
                                       0.95, max_retries=2, crop=(470 / 1920, 0, 970 / 1920, 114 / 1080))
                    if auto.click_element("./assets/images/screen/forgottenhall/memory_of_chaos.png", "image",
                                          0.95, max_retries=10, crop=(36 / 1920, 25 / 1080, 170 / 1920, 80 / 1080)):
                        flag = True

        if not flag:
            screen.change_to('menu')
            return False

        # 刷新后打开会出现本期buff的弹窗
        time.sleep(2)
        if auto.find_element("./assets/images/base/click_close.png", "image", 0.8):
            # 等待不可点击的动画时间
            time.sleep(2)
            auto.click_element("./assets/images/base/click_close.png", "image", 0.8, max_retries=8)
            auto.click_element("./assets/images/screen/forgottenhall/memory_of_chaos.png", "image",
                               0.95, max_retries=10, crop=(36 / 1920, 25 / 1080, 170 / 1920, 80 / 1080))

        ForgottenHall.run()

        screen.change_to('main')
        return True
    
    def get_star_and_level():
        screen.change_to('guide3')
        guide3_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        if auto.click_element("侵蚀隧洞", "text", max_retries=10, crop=guide3_crop):
            auto.mouse_scroll(12, -1)
            if auto.click_element("忘却之庭", "text", max_retries=10, crop=guide3_crop):
                time.sleep(1)
                countdownTextCrop=(1425.0 / 1920, 319.0 / 1080, 199.0 / 1920, 43.0 / 1080)
                levelTextCrop=(1346.0 / 1920, 646.0 / 1080, 67.0 / 1920, 37.0 / 1080)
                starTextCrop = (1345.0 / 1920, 693.0 / 1080, 68.0 / 1920, 29.0 / 1080)
                try:
                    time.sleep(0.5)
                    countdownText = auto.get_single_line_text(crop=countdownTextCrop, blacklist=[], max_retries=6)
                    countdownText = countdownText.replace('）','').replace(')','').replace('①','')
                    if countdownText == '?':
                        countdownText = '识别出错'
                    levelText = auto.get_single_line_text(crop=levelTextCrop, blacklist=[], max_retries=3)
                    starText = auto.get_single_line_text(crop=starTextCrop, blacklist=[], max_retries=3)
                    logger.info(f"忘却之庭刷新倒计时:{countdownText},层数:{levelText},星数:{starText}")
                    Utils._content['countdownText'] = countdownText
                    level = levelText.split('/')[0]
                    star = starText.split('/')[0]
                    config.forgottenhall_levels[Utils.get_uid()] = int(level)
                    config.forgottenhall_stars[Utils.get_uid()] = int(star)
                    config.save_config()
                except Exception as e:
                    logger.error(_("识别忘却之庭失败: {error}").format(error=e))
                    logger.warning(_("因读取忘却之庭失败,程序中止"))

        screen.change_to('main')
        return True

    @staticmethod
    def start():
        logger.hr(_("准备混沌回忆"), 2)

        if ForgottenHall.prepare():
            # Utils.detectTimestamp(config.forgottenhall_timestamp, Utils.get_uid())
            Utils.saveTimestamp('forgottenhall_timestamp', Utils.get_uid())
            logger.info(_("混沌回忆完成"))

    @staticmethod
    def start_memory_one():
        try:
            flag = False
            logger.hr(_("准备回忆一"), 2)
            screen.change_to("memory")
            auto.mouse_scroll(30, 1)
            time.sleep(2)
            if auto.click_element("01", "text", max_retries=20, crop=(18.0 / 1920, 226.0 / 1080, 1896.0 / 1920, 656.0 / 1080)):
                if auto.find_element("./assets/images/forgottenhall/team1.png", "image", 0.8, max_retries=10, crop=(610 / 1920, 670 / 1080, 118 / 1920, 218 / 1080)):
                    # auto.take_screenshot(crop=(30 / 1920, 115 / 1080, 530 / 1920, 810 / 1080))
                    char_count=0
                    auto.click_element_with_pos(((70, 300),(70, 300)), action="move")
                    for character in config.daily_memory_one_team:
                        time.sleep(0.5)
                        if char_count == 4:
                            break
                        logger.info(f"{character[0]}")
                        if not auto.click_element(f"./assets/images/character/{character[0]}.png", "image", 0.9, max_retries=10, take_screenshot=True):
                            auto.mouse_scroll(15, -1)
                            if not auto.click_element(f"./assets/images/character/{character[0]}.png", "image", 0.9, max_retries=10, take_screenshot=True):
                                auto.mouse_scroll(15, 1)
                                continue
                            else:
                                logger.info("该角色已选中")
                                auto.mouse_scroll(15, 1)
                                char_count+=1
                        else:
                            logger.info("该角色已选中")
                            char_count+=1
                        time.sleep(0.5)
                    if auto.click_element("回忆", "text", max_retries=10, crop=(1546 / 1920, 962 / 1080, 343 / 1920, 62 / 1080), include=True):
                        ForgottenHall.click_message_box()
                        if ForgottenHall.start_fight(1, 1, 0, config.daily_memory_one_team):
                            flag = True
            time.sleep(2)
            logger.info(_("回忆一完成"))
            return flag
        except Exception as e:
            logger.error(_("回忆一失败: {error}").format(error=e))
            return False

    @staticmethod
    def finish_forgottenhall():
        if config.daily_memory_one_enable:
            return ForgottenHall.start_memory_one()

    @staticmethod
    def weakness_to_fight():
        if config.daily_memory_one_enable:
            if config.daily_tasks_fin[Utils.get_uid()]:
                logger.info(_("每日活跃度已满,跳过"))
                return False
            logger.info(_("进行[利用弱点进入战斗并获胜3次]"))
            return ForgottenHall.start_memory_one() and ForgottenHall.start_memory_one() and ForgottenHall.start_memory_one()

    @staticmethod
    def weakness_3():
        if config.daily_memory_one_enable:
            if config.daily_tasks_fin[Utils.get_uid()]:
                logger.info(_("每日活跃度已满,跳过"))
                return False
            logger.info(_("进行[单场战斗中，触发3种不同属性的弱点击破]"))
            return ForgottenHall.start_memory_one()

    @staticmethod
    def weakness_5():
        if config.daily_memory_one_enable:
            if config.daily_tasks_fin[Utils.get_uid()]:
                logger.info(_("每日活跃度已满,跳过"))
                return False
            logger.info(_("进行[累计触发弱点击破效果5次]"))
            return ForgottenHall.start_memory_one()

    @staticmethod
    def enemy_20():
        if config.daily_memory_one_enable:
            if config.daily_tasks_fin[Utils.get_uid()]:
                logger.info(_("每日活跃度已满,跳过"))
                return False
            logger.info(_("进行[累计消灭20个敌人]"))
            return ForgottenHall.start_memory_one() and ForgottenHall.start_memory_one() and ForgottenHall.start_memory_one()

    @staticmethod
    def ultimate():
        if config.daily_memory_one_enable:
            if config.daily_tasks_fin[Utils.get_uid()]:
                logger.info(_("每日活跃度已满,跳过"))
                return False
            logger.info(_("进行[施放终结技造成制胜一击1次]"))
            return ForgottenHall.start_memory_one()
