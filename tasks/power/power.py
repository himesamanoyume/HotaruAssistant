from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.logger_manager import logger
from managers.config_manager import config
from tasks.daily.utils import Utils
from managers.translate_manager import _
from tasks.base.base import Base
import time


class Power:
    @staticmethod
    def start():
        instance_name = config.instance_names[Utils.get_uid()][config.instance_type[Utils.get_uid()]]
        if instance_name == "无":
            logger.info(_("跳过清体力 {type}未开启").format(type=config.instance_type[Utils.get_uid()]))
            return False

        logger.hr(_("开始清体力"), 0)

        # 兼容旧设置
        if "·" in instance_name:
            instance_name = instance_name.split("·")[0]

        Power.instance(config.instance_type[Utils.get_uid()], instance_name, config.power_needs[config.instance_type[Utils.get_uid()]])
        logger.hr(_("完成"), 2)

    @staticmethod
    def power():
        def get_power(crop, type="trailblaze_power"):
            try:
                if type == "trailblaze_power":
                    result = auto.get_single_line_text(crop=crop, blacklist=['+', '米'], max_retries=3)
                    power = int(result.replace("1240", "/240").split('/')[0])
                    return power if 0 <= power <= 999 else -1
                elif type == "reserved_trailblaze_power":
                    result = auto.get_single_line_text(crop=crop, blacklist=['+', '米'], max_retries=3)
                    power = int(result[0])
                    return power if 0 <= power <= 2400 else -1
            except Exception as e:
                logger.error(_("识别开拓力失败: {error}").format(error=e))
                return -1

        def move_button_and_confirm():
            if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=10):
                result = auto.find_element("./assets/images/share/trailblaze_power/button.png", "image", 0.9, max_retries=10)
                if result:
                    auto.click_element_with_pos(result, action="down")
                    time.sleep(0.5)
                    result = auto.find_element("./assets/images/share/trailblaze_power/plus.png", "image", 0.9)
                    if result:
                        auto.click_element_with_pos(result, action="move")
                        time.sleep(0.5)
                        auto.mouse_up()
                        if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=10):
                            time.sleep(1)
                            auto.press_key("esc")
                            if screen.check_screen("map"):
                                return True
            return False

        trailblaze_power_crop = (1588.0 / 1920, 35.0 / 1080, 198.0 / 1920, 56.0 / 1080)

        if config.use_reserved_trailblaze_power or config.use_fuel:
            screen.change_to('map')
            # 打开开拓力补充界面
            if auto.click_element("./assets/images/share/trailblaze_power/trailblaze_power.png", "image", 0.9, crop=trailblaze_power_crop):
                # 等待界面加载
                if auto.find_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=10):
                    # 开启使用后备开拓力
                    if config.use_reserved_trailblaze_power and auto.click_element("./assets/images/share/trailblaze_power/reserved_trailblaze_power.png", "image", 0.9, scale_range=(0.95, 0.95)):
                        move_button_and_confirm()
                    # 开启使用燃料
                    elif config.use_fuel and auto.click_element("./assets/images/share/trailblaze_power/fuel.png", "image", 0.9, scale_range=(0.95, 0.95)):
                        move_button_and_confirm()
                    # # 开启使用星琼
                    # elif config.stellar_jade and auto.click_element("./assets/images/share/trailblaze_power/stellar_jade.png", "image", 0.9, scale_range=(0.95, 0.95)):
                    #     pass
                    else:
                        auto.press_key("esc")

        screen.change_to('map')
        trailblaze_power = get_power(trailblaze_power_crop)

        logger.info(_("🟣开拓力: {power}").format(power=trailblaze_power))
        logger.info(_("开拓力回满时间为:{time}").format(time=Utils.getFullPowerTime(trailblaze_power)))
        return trailblaze_power

    @staticmethod
    def wait_fight():
        logger.info(_("进入战斗"))

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
            return auto.find_element("./assets/images/fight/fight_again.png", "image", 0.9)
        if not auto.retry_with_timeout(lambda: check_fight(), 30 * 60, 1):
            logger.error(_("战斗超时"))
            raise Exception(_("战斗超时"))
        logger.info(_("战斗完成"))

    @staticmethod
    def borrow_character():
        if not (("使用支援角色并获得战斗胜利1次" in config.daily_tasks[Utils.get_uid()] and config.daily_tasks[Utils.get_uid()]["使用支援角色并获得战斗胜利1次"]) or config.borrow_character_enable):
            return True
        if not auto.click_element("支援", "text", max_retries=10, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            logger.error(_("找不到支援按钮"))
            return False
        # 等待界面加载
        time.sleep(0.5)
        if not auto.find_element("支援列表", "text", max_retries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080)):
            logger.error(_("未进入支援列表"))
            return False

        try:
            # 尝试优先使用指定用户名的支援角色
            if config.borrow_character_from:
                auto.click_element("UID", "text", max_retries=10, crop=(18.0 / 1920, 15.0 / 1080, 572.0 / 1920, 414.0 / 1080), include=True)
                time.sleep(0.5)
                for i in range(3):
                    if auto.click_element(config.borrow_character_from, "text", crop=(196 / 1920, 167 / 1080, 427 / 1920, 754 / 1080), include=True):
                        # 找到角色的对应处理
                        if not auto.click_element("入队", "text", max_retries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                            logger.error(_("找不到入队按钮"))
                            return False
                        # 等待界面加载
                        time.sleep(0.5)
                        result = auto.find_element(("解除支援", "取消"), "text", max_retries=10, include=True)
                        if result:
                            if auto.matched_text == "解除支援":
                                if "使用支援角色并获得战斗胜利1次" in config.daily_tasks[Utils.get_uid()]:
                                    config.daily_tasks[Utils.get_uid()]["使用支援角色并获得战斗胜利1次"] = False
                                config.save_config()
                                return True
                            elif auto.matched_text == "取消":
                                auto.click_element_with_pos(result)
                                auto.find_element("支援列表", "text", max_retries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080))
                                continue
                        else:
                            return False
                    auto.mouse_scroll(27, -1)
                    # 等待界面完全停止
                    time.sleep(0.5)

                logger.info(_("找不到指定用户名的支援角色，尝试按照优先级选择"))
                # 重新打开支援页面，防止上一次的滚动位置影响
                auto.press_key("esc")
                time.sleep(0.5)
                if not auto.click_element("支援", "text", max_retries=10, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
                    logger.error(_("找不到支援按钮"))
                    return False
                # 等待界面加载
                time.sleep(0.5)
                if not auto.find_element("支援列表", "text", max_retries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080)):
                    logger.error(_("未进入支援列表"))
                    return False

            for name in config.borrow_character:
                if auto.click_element("./assets/images/character/" + name + ".png", "image", 0.8, max_retries=1, scale_range=(0.9, 0.9), crop=(57 / 1920, 143 / 1080, 140 / 1920, 814 / 1080)):
                    if not auto.click_element("入队", "text", max_retries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                        logger.error(_("找不到入队按钮"))
                        return False
                    # 等待界面加载
                    time.sleep(0.5)
                    result = auto.find_element(("解除支援", "取消"), "text", max_retries=10, include=True)
                    if result:
                        if auto.matched_text == "解除支援":
                            config.daily_tasks[Utils.get_uid()]["使用支援角色并获得战斗胜利1次"] = False
                            config.save_config()
                            return True
                        elif auto.matched_text == "取消":
                            auto.click_element_with_pos(result)
                            auto.find_element("支援列表", "text", max_retries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080))
                            continue
                    else:
                        return False
        except Exception as e:
            logger.warning(_("选择支援角色出错： {e}").format(e=e))

        auto.press_key("esc")
        if auto.find_element("解除支援", "text", max_retries=2, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            return True
        else:
            return False

    @staticmethod
    def run_instances(instance_type, instance_name, a_times_need_power, total_count):
        if instance_name == "无":
            logger.debug(_("{type}未开启").format(type=instance_type))
            return False

        instance_name = instance_name.replace("巽风之形", "风之形")
        instance_name = instance_name.replace("翼风之形", "风之形")

        instance_name = instance_name.replace("偃偶之形", "偶之形")
        instance_name = instance_name.replace("孽兽之形", "兽之形")

        instance_name = instance_name.replace("燔灼之形", "灼之形")
        instance_name = instance_name.replace("潘灼之形", "灼之形")
        instance_name = instance_name.replace("熠灼之形", "灼之形")

        if config.instance_team_enable:
            Base.change_team(config.instance_team_number)

        screen.change_to('guide3')
        instance_type_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        if not auto.click_element(instance_type, "text", crop=instance_type_crop):
            if auto.click_element("侵蚀隧洞", "text", max_retries=10, crop=instance_type_crop):
                auto.mouse_scroll(12, -1)
                auto.click_element(instance_type, "text", crop=instance_type_crop)
        # 截图过快会导致结果不可信
        time.sleep(1)

        # 传送
        instance_name_crop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
        auto.click_element("./assets/images/screen/guide/power.png", "image", max_retries=10)
        Flag = False
        for i in range(5):
            if auto.click_element("传送", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name):
                Flag = True
                break
            auto.mouse_scroll(18, -1)
            # 等待界面完全停止
            time.sleep(0.5)
        if not Flag:
            Base.send_notification_with_screenshot(_("⚠️刷副本未完成 - 没有找到指定副本名称⚠️"))
            return False
        # 验证传送是否成功
        if not auto.find_element(instance_name, "text", max_retries=20, include=True, crop=(1172.0 / 1920, 5.0 / 1080, 742.0 / 1920, 636.0 / 1080)):
            Base.send_notification_with_screenshot(_("⚠️刷副本未完成 - 传送可能失败⚠️"))
            return False

        if "拟造花萼" in instance_type:
            full_count = total_count // 6
            incomplete_count = total_count - full_count * 6
            if not 0 <= full_count or not 0 <= incomplete_count <= 6:
                Base.send_notification_with_screenshot(_("⚠️刷副本未完成 - 拟造花萼次数错误⚠️"))
                return False
            result = auto.find_element("./assets/images/screen/guide/plus.png", "image", 0.9, max_retries=10,
                                       crop=(1174.0 / 1920, 775.0 / 1080, 738.0 / 1920, 174.0 / 1080))
            if full_count == 0:
                for i in range(incomplete_count - 1):
                    auto.click_element_with_pos(result)
                    time.sleep(0.5)
            else:
                for i in range(5):
                    auto.click_element_with_pos(result)
                    time.sleep(0.5)

        if auto.click_element("挑战", "text", max_retries=10, need_ocr=True):
            if instance_type == "历战余响":
                time.sleep(1)
                auto.click_element("./assets/images/base/confirm.png", "image", 0.9)
            Power.borrow_character()
            if auto.click_element("开始挑战", "text", max_retries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                if instance_type == "凝滞虚影":
                    time.sleep(2)
                    for i in range(3):
                        auto.press_mouse()
                
                for i in range(full_count - 1):
                    Power.wait_fight()
                    logger.info(_("第{number}次副本完成").format(number=i+1))
                    auto.click_element("./assets/images/fight/fight_again.png", "image", 0.9, max_retries=10)
                    if instance_type == "历战余响":
                        time.sleep(1)
                        auto.click_element("./assets/images/base/confirm.png", "image", 0.9)
                
                Power.wait_fight()
                if full_count > 0:
                    logger.info(_("{number}次副本完成").format(number=full_count*6))
                else:
                    logger.info(_("{number}次副本完成").format(number=incomplete_count))
                # 速度太快，点击按钮无效
                time.sleep(1)
                auto.click_element("./assets/images/fight/fight_exit.png", "image", 0.9, max_retries=10)
                time.sleep(2)
                if full_count > 0 and incomplete_count > 0:
                    Power.run_instances(instance_type, instance_name, a_times_need_power, incomplete_count)
                else:
                    logger.info(_("副本任务完成"))
                    return True
                

    @staticmethod
    def instance(instance_type, instance_name, power_need, number=None):
        if instance_name == "无":
            logger.debug(_("{type}未开启").format(type=instance_type))
            return False
        logger.hr(_("准备{type}").format(type=instance_type), 2)
        power = Power.power()
        if number is None:
            # number刷的次数
            number = power // power_need
            if number < 1:
                logger.info(_("🟣开拓力 < {power_need}").format(power_need=power_need))
                return False
        else:
            if power_need * number > power:
                logger.info(_("🟣开拓力 < {power_need}*{number}").format(power_need=power_need, number=number))
                return False

        logger.hr(_("开始刷{type} - {name}，总计{number}次").format(type=instance_type, name=instance_name, number=number), 2)
        return Power.run_instances(instance_type, instance_name, power_need, number)
