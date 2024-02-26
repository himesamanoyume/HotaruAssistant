from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.logger_manager import logger
from managers.config_manager import config
from tasks.daily.utils import Utils
from managers.translate_manager import _
from managers.utils_manager import gu
from tasks.daily.relics import Relics
from tasks.base.base import Base
import time


class Power:
    @staticmethod
    def start(): 
        if config.instance_type[Utils.get_uid()][0] == '模拟宇宙':
            Utils._power = Power.power()
            return
        else:
            instance_name = config.instance_names[Utils.get_uid()][config.instance_type[Utils.get_uid()][0]]
            if instance_name == "无":
                logger.info(gu(f"跳过清体力,{config.instance_type[Utils.get_uid()][0]}未开启"))
                return False
        
        Relics.detect_relic_count()
        Relics.skip_for_relic_count()
        if Utils._power<=8:
            logger.info(gu(f"跳过清体力,体力太低"))
            return
     
        logger.hr(gu("开始清体力"), 0)

        # 兼容旧设置
        if "·" in instance_name:
            instance_name = instance_name.split("·")[0]

        Power.instance(config.instance_type[Utils.get_uid()][0], instance_name, config.power_needs[config.instance_type[Utils.get_uid()][0]])
        logger.hr(gu("完成"), 2)

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
            logger.error(gu(f"识别开拓力失败: {e}"))
            return -1

    @staticmethod
    def power():
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
        trailblaze_power = Power.get_power(trailblaze_power_crop)
        Utils._power = trailblaze_power
        logger.info(gu(f"🟣开拓力: {trailblaze_power}"))
        Utils._content.update({'new_power':f'{trailblaze_power}'})
        logger.info(gu(f"开拓力回满时间为:{Utils.getFullPowerTime(trailblaze_power)}"))
        Utils._content.update({'full_power_time':f'{Utils.getFullPowerTime(trailblaze_power)}'})
        return trailblaze_power

    @staticmethod
    def wait_fight(instance_name):
        logger.info(gu("进入战斗"))
        time.sleep(5)
        for i in range(20):
            if auto.find_element("./assets/images/base/2x_speed_on.png", "image", 0.9, crop=(1618.0 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
                logger.info(gu("二倍速已开启"))
                break
            else:
                logger.info(gu("尝试开启二倍速"))
                auto.press_key("b")
                time.sleep(0.5)
                if auto.find_element("./assets/images/fight/fight_again.png", "image", 0.9) or auto.find_element("./assets/images/fight/fight_fail.png", "image", 0.9):
                    break

        time.sleep(5)

        for i in range(20):
            if auto.find_element("./assets/images/base/not_auto.png", "image", 0.95):
                logger.info(gu("尝试开启自动战斗"))
                auto.press_key("v")
                time.sleep(0.5)
                if auto.find_element("./assets/images/fight/fight_again.png", "image", 0.9) or auto.find_element("./assets/images/fight/fight_fail.png", "image", 0.9):
                    break
            elif auto.find_element("./assets/images/base/auto.png", "image", 0.985, take_screenshot=False):
                logger.info(gu("自动战斗已开启"))
                break
        time.sleep(1)

        logger.info(gu("等待战斗"))
        Power.isFightFail = False

        def check_fight():
            if auto.find_element("./assets/images/fight/fight_fail.png", "image", 0.9):
                Power.isFightFail = True

            return auto.find_element("./assets/images/fight/fight_again.png", "image", 0.9) or auto.find_element("./assets/images/fight/fight_fail.png", "image", 0.9)
                  
        if not auto.retry_with_timeout(lambda: check_fight(), 10 * 60, 1):
            nowtime = time.time()
            logger.error(gu(f"{nowtime},挑战{instance_name}时战斗超时或战败"))
            raise Exception(f"{nowtime},挑战{instance_name}时战斗超时或战败")
        else:
            if Power.isFightFail:
                auto.click_element("./assets/images/fight/fight_fail.png", "image", 0.9)
                nowtime = time.time()
                logger.error(gu(f"{nowtime},挑战{instance_name}时战败,请检查当前队伍练度,可能是当前队伍搭配不好打该副本,也可能是生存位被集火阵亡最终导致全队阵亡"))
                raise Exception(f"{nowtime},挑战{instance_name}时战败,请检查当前队伍练度,可能是当前队伍搭配不好打该副本,也可能是生存位被集火阵亡最终导致全队阵亡")
            else:
                logger.info(gu("战斗完成"))

    @staticmethod
    def borrow_character():
        if not (("使用支援角色并获得战斗胜利1次" in config.daily_tasks[Utils.get_uid()] and config.daily_tasks[Utils.get_uid()]["使用支援角色并获得战斗胜利1次"]) or config.borrow_character_enable):
            return True
        if not auto.click_element("支援", "text", max_retries=10, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            logger.error(gu("找不到支援按钮"))
            return False
        # 等待界面加载
        time.sleep(0.5)
        if not auto.find_element("支援列表", "text", max_retries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080)):
            logger.error(gu("未进入支援列表"))
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
                            logger.error(gu("找不到入队按钮"))
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
                    time.sleep(1)

                logger.info(gu("找不到指定用户名的支援角色，尝试按照优先级选择"))
                # 重新打开支援页面，防止上一次的滚动位置影响
                auto.press_key("esc")
                time.sleep(0.5)
                if not auto.click_element("支援", "text", max_retries=10, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
                    logger.error(gu("找不到支援按钮"))
                    return False
                # 等待界面加载
                time.sleep(0.5)
                if not auto.find_element("支援列表", "text", max_retries=10, crop=(234 / 1920, 78 / 1080, 133 / 1920, 57 / 1080)):
                    logger.error(gu("未进入支援列表"))
                    return False

            for name in config.borrow_character:
                if auto.click_element("./assets/images/character/" + name + ".png", "image", 0.8, max_retries=1, scale_range=(0.9, 0.9), crop=(57 / 1920, 143 / 1080, 140 / 1920, 814 / 1080)):
                    if not auto.click_element("入队", "text", max_retries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                        logger.error(gu("找不到入队按钮"))
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
            logger.warning(gu(f"选择支援角色出错： {e}"))

        auto.press_key("esc")
        if auto.find_element("解除支援", "text", max_retries=2, crop=(1670 / 1920, 700 / 1080, 225 / 1920, 74 / 1080)):
            return True
        else:
            return False
        
    @staticmethod
    def run_instances(instance_type, instance_name, a_times_need_power, total_count):
        if instance_name == "无":
            logger.warning(gu(f"{instance_type}未开启"))
            return False

        instance_name = instance_name.replace("巽风之形", "风之形")
        instance_name = instance_name.replace("翼风之形", "风之形")

        instance_name = instance_name.replace("偃偶之形", "偶之形")
        instance_name = instance_name.replace("孽兽之形", "兽之形")

        instance_name = instance_name.replace("燔灼之形", "灼之形")
        instance_name = instance_name.replace("潘灼之形", "灼之形")
        instance_name = instance_name.replace("熠灼之形", "灼之形")
        instance_name = instance_name.replace("蛀星的旧靥", "蛀星的旧")

        if config.instance_team_enable:
            Base.change_team(config.instance_team_number)

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
        instance_map_type = ''
        import json
        rb = open("./assets/config/ruby_detail.json", 'r', encoding='utf-8')
        ruby = json.load(rb)
        rb.close()

        if instance_type in ['拟造花萼（赤）']:
            source = f"./assets/images/screen/guide/aka/{ruby['拟造花萼（赤）'][instance_name]}.png"
            for i in range(7):
                if auto.click_element("传送", "min_distance_text", crop=instance_name_crop, include=True, source=source,  source_type="image"):
                    Flag = True
                    break

                elif auto.click_element("进入", "min_distance_text", crop=instance_name_crop, include=True, source=source,  source_type="image"):
                    logger.info("该副本限时开放中,但你并没有解锁该副本")
                    Flag = True
                    break

                if auto.click_element("追踪", "min_distance_text", crop=instance_name_crop, include=True, source=source,  source_type="image"):
                    nowtime = time.time()
                    logger.error(gu(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                    raise Exception(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本")
                    
                auto.mouse_scroll(18, -1)
                # 等待界面完全停止
                time.sleep(1)
        elif instance_type in ['拟造花萼（金）']:

            instance_map, instance_map_type = instance_name.split('-')
            instance_map_name = ruby['星球'][instance_map]

            for i in range(2):
                if auto.click_element(f"./assets/images/screen/guide/{instance_map_name}_on.png", "image", 0.9, max_retries=10) or auto.click_element(f"./assets/images/screen/guide/{instance_map_name}_off.png", "image", 0.9, max_retries=10):

                    if auto.click_element("传送", "min_distance_text", crop=instance_name_crop, include=True, source=instance_map_type):
                        Flag = True
                        break

                    elif auto.click_element("进入", "min_distance_text", crop=instance_name_crop, include=True, source=instance_map_type, source_type="text"):
                        logger.info("该副本限时开放中,但你并没有解锁该副本")
                        Flag = True
                        break

                    if auto.click_element("追踪", "min_distance_text", crop=instance_name_crop, include=True, source=instance_map_type, source_type="text"):
                        nowtime = time.time()
                        logger.error(gu(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                        raise Exception(f"{nowtime},{instance_map_type}:你似乎没有解锁这个副本?总之无法传送到该副本")
                    
                # 等待界面完全停止
                time.sleep(1)     
        else:
            for i in range(7):
                if auto.click_element("传送", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name, source_type="text"):
                    Flag = True
                    break
                elif auto.click_element("进入", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name, source_type="text"):
                    logger.info("该副本限时开放中,但你并没有解锁该副本")
                    Flag = True
                    break

                if auto.click_element("追踪", "min_distance_text", crop=instance_name_crop, include=True, source=instance_name, source_type="text"):
                    nowtime = time.time()
                    logger.error(gu(f"{nowtime},{instance_name}:你似乎没有解锁这个副本?总之无法传送到该副本"))
                    raise Exception(f"{nowtime},{instance_name}:你似乎没有解锁这个副本?总之无法传送到该副本")
                auto.mouse_scroll(18, -1)
                # 等待界面完全停止
                time.sleep(1)
            
        if not Flag:
            logger.error(gu("⚠️刷副本未完成 - 没有找到指定副本名称⚠️"))

            return False
        # 验证传送是否成功
        if not auto.find_element(instance_name.replace("2", ""), "text", max_retries=20, include=True, crop=(1172.0 / 1920, 5.0 / 1080, 742.0 / 1920, 636.0 / 1080)):
            if not auto.find_element(instance_map_type, "text", max_retries=20, include=True, crop=(1172.0 / 1920, 5.0 / 1080, 742.0 / 1920, 636.0 / 1080)):
                logger.error(gu("⚠️刷副本未完成 - 传送可能失败⚠️"))
                return False

        full_count = total_count // 6
        incomplete_count = total_count - full_count * 6
        logger.info(gu(f"按单次体力需求计算次数:{total_count},按6次为完整一次计算:{full_count},按扣除完整次数剩下次数计算:{incomplete_count}"))
        if "拟造花萼" in instance_type:
            
            if not 0 <= full_count or not 0 <= incomplete_count <= 6:
                logger.error(gu("⚠️刷副本未完成 - 拟造花萼次数错误⚠️"))
                # Base.send_notification_with_screenshot(_("⚠️刷副本未完成 - 拟造花萼次数错误⚠️"))
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

            if config.daily_tasks_fin[Utils.get_uid()] == False:
                Power.borrow_character()
            if auto.click_element("开始挑战", "text", max_retries=10, crop=(1518 / 1920, 960 / 1080, 334 / 1920, 61 / 1080)):
                time.sleep(1)

                if auto.find_element("./assets/images/fight/no_power.png", "image", 0.9):
                    nowtime = time.time()
                    logger.error(gu(f"{nowtime},挑战{instance_name}时开拓力不足,但却触发了挑战,请检查"))
                    raise Exception(f"{nowtime},挑战{instance_name}时开拓力不足,但却触发了挑战,请检查")
                
                if auto.find_element("./assets/images/fight/char_dead.png", "image", 0.9):
                    nowtime = time.time()
                    logger.error(gu(f"{nowtime},挑战{instance_name}时有角色处于无法战斗的状态,请检查"))
                    raise Exception(f"{nowtime},挑战{instance_name}时有角色处于无法战斗的状态,请检查")
                
                if instance_type in ["凝滞虚影", "侵蚀隧洞", "历战余响"]:
                    time.sleep(2)
                    if instance_type in ["凝滞虚影"]:
                        for i in range(3):
                            auto.press_mouse()
                            time.sleep(3)

                    for i in range(total_count - 1):
                        Power.wait_fight(instance_name)
                        logger.info(gu(f"第{i+1}次{instance_type}副本完成(1)"))
                        if instance_type == "侵蚀隧洞":
                            Relics.instance_get_relic()
                        time.sleep(1)
                        auto.click_element("./assets/images/fight/fight_again.png", "image", 0.9, max_retries=10)
                        if instance_type == "历战余响":
                            time.sleep(1)
                            auto.click_element("./assets/images/base/confirm.png", "image", 0.9) 
                        time.sleep(1) 
                else:
                    if full_count > 0:
                        for i in range(full_count - 1):
                            Power.wait_fight(instance_name)
                            logger.info(gu(f"第{i+1}次{instance_type}副本完成(2)"))
                            if not (full_count == 1 and incomplete_count == 0):
                                auto.click_element("./assets/images/fight/fight_again.png", "image", 0.9, max_retries=10)
                                # if instance_type == "历战余响":
                                #     time.sleep(1)
                                #     auto.click_element("./assets/images/base/confirm.png", "image", 0.9)  
                
                Power.wait_fight(instance_name)
                if instance_type == "侵蚀隧洞":
                    Relics.instance_get_relic()
                if full_count > 0:
                    logger.info(gu(f"{full_count*6}次{instance_type}副本完成(3)"))
                elif instance_type == "凝滞虚影" or "侵蚀隧洞" :
                    logger.info(gu(f"{total_count}次{instance_type}副本完成(4)"))
                else:
                    logger.info(gu(f"{incomplete_count}次{instance_type}副本完成(5)"))
                # 速度太快，点击按钮无效
                time.sleep(1)
                auto.click_element("./assets/images/fight/fight_exit.png", "image", 0.9, max_retries=10)
                time.sleep(2)
                if full_count > 0 and incomplete_count > 0:
                    Power.run_instances(instance_type, instance_name, a_times_need_power, incomplete_count)
                else:
                    logger.info(gu("副本任务完成"))
                    return True

    @staticmethod
    def instance(instance_type, instance_name, power_need, number=None):
        if instance_name == "无":
            logger.warning(gu(f"{instance_type}未开启"))
            return False
        logger.hr(gu(f"准备{instance_type}"), 2)
        power = Power.power()
        if number is None:
            # number刷的次数
            number = power // power_need
            if number < 1:
                logger.info(gu(f"🟣开拓力 < {power_need}"))
                return False
        else:
            if power_need * number > power:
                logger.info(gu(f"🟣开拓力 < {power_need}*{number}"))
                return False
        
        Utils._temp += "<p>"+f'{instance_type} - {instance_name} - {number}次</p>'

        logger.hr(gu(f"开始刷{instance_type} - {instance_name}，总计{number}次"), 2)
        return Power.run_instances(instance_type, instance_name, power_need, number)
