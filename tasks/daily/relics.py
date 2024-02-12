from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.logger_manager import logger
from managers.utils_manager import gu
from managers.ocr_manager import ocr
from managers.config_manager import config
from managers.translate_manager import _
from tasks.daily.utils import Utils
import time

class Relics:
    @staticmethod
    def skip_for_relic_count():
        if Utils._relicCount >= config.relic_threshold_count[Utils.get_uid()]:
            nowtime = time.time()
            logger.error(gu(f"{nowtime},检测到遗器数量超过{config.relic_threshold_count[Utils.get_uid()]},所有可能获得遗器的副本全部跳过,出现该致命错误意味着你没有选择开启遗器自动分解开关,若不打算开启,则只能自行上号清理,否则每次上号时遗器数量超标时都会直接中止"))
            raise Exception(f"{nowtime},检测到遗器数量超过{config.relic_threshold_count[Utils.get_uid()]},所有可能获得遗器的副本全部跳过,出现该致命错误意味着你没有选择开启遗器自动分解开关,若不打算开启,则只能自行上号清理,否则每次上号时遗器数量超标时都会直接中止")

    @staticmethod
    def salvage():
        try:
            logger.hr(gu("准备分解遗器"), 2)
            # screen.get_current_screen()
            if not config.relic_salvage_enable[Utils.get_uid()]:
                logger.info(gu("检测到分解遗器未开启,跳过分解遗器"))
                return
            screen.change_to('bag_relics')
            if auto.click_element("分解", "text", max_retries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                if auto.click_element("分解", "text", max_retries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                    time.sleep(1)
                    if auto.click_element("./assets/images/relic/fast_select.png", "image", 0.9, max_retries=10):
                        # 等待筛选界面弹出
                        time.sleep(1)
                        fast_select_crop=(439.0 / 1920, 357.0 / 1080, 1018.0 / 1920, 448.0 / 1080)
                        auto.click_element("全选已弃置", "text", max_retries=10, crop=fast_select_crop)
                        time.sleep(0.5)
                        auto.click_element("3星及以下", "text", max_retries=10, crop=fast_select_crop)
                        time.sleep(0.5)
                        if config.relic_salvage_4star_enable[Utils.get_uid()]:
                            auto.click_element("4星及以下", "text", max_retries=10, crop=fast_select_crop)
                            time.sleep(0.5)
                        if config.relic_salvage_5star_enable[Utils.get_uid()]:
                            auto.click_element("5星及以下", "text", max_retries=10, crop=fast_select_crop)
                            time.sleep(0.5)
                        if auto.click_element("确认", "text", max_retries=10, crop=fast_select_crop):
                            time.sleep(3)
                            countText = auto.get_single_line_text((616.0 / 1920, 871.0 / 1080, 110.0 / 1920, 37.0 / 1080), [], 5)
                            count = countText.split('/')[0]
                            logger.info(gu(f"已选数量:{count}/500"))
                            time.sleep(0.5)
                            if count != 0:
                                if config.relic_salvage_5star_enable[Utils.get_uid()] and config.relic_salvage_5star_to_exp[Utils.get_uid()]:
                                    if auto.click_element("./assets/images/relic/relic_exp.png", "image", 0.9, max_retries=10):
                                        logger.info("已点击将5星遗器分解为遗器经验材料")
                                time.sleep(1)
                                if auto.click_element("./assets/images/relic/salvage.png", "image", max_retries=10):
                                    logger.info(gu(f"已点击分解遗器"))
                                    time.sleep(1)
                                    if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=10):
                                        logger.info(gu(f"已点击确认"))
                                        time.sleep(1)
                                        if auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10):
                                            logger.info(gu(f"已点击关闭窗口"))
                                            time.sleep(1)
                                            logger.info(gu(f"分解遗器{count}件完成"))
                                            screen.change_to('main')
                                            return True
                            else:
                                logger.error(gu("分解遗器失败: 没有多余的遗器可供分解"))
                                screen.change_to('main')
                                return False
                logger.error(gu("分解遗器失败"))
                return False
        except Exception as e:
            logger.error(gu(f"分解遗器失败: {e}"))
            return False
    
    @staticmethod
    def detect_relic_count():
        try:
            logger.hr(gu("准备检测遗器数量"), 2)
            # screen.get_current_screen()
            screen.change_to('bag_relics')
            relic_count_crop=(1021.0 / 1920, 974.0 / 1080, 131.0 / 1920, 33.0 / 1080)
            relic_countText = auto.get_single_line_text(relic_count_crop, ['遗','器','数','量'], max_retries=5)
            relic_countText = relic_countText.replace('量','')
            logger.info(gu(f"遗器数量:{relic_countText}"))
            relic_countText = relic_countText.split('/')[0]
            Utils._relicCount = int(relic_countText)
            if Utils._relicCount >= config.relic_threshold_count[Utils.get_uid()]:
                logger.warning(gu("检测到遗器数量超标"))
                Relics.salvage()
                Relics.detect_relic_count()

        except Exception as e:
            logger.error(gu(f"检测遗器数量失败: {e}"))
        return False
    
    @staticmethod
    def create_relic_content(relicName, relicPart, relicList):
        logger.info(gu("正在生成胚子信息"))
        Utils._content['relic_content'] += f"<div class=relic><p><strong>{relicName}</strong><span style=font-size:10px>{relicPart}</span></p>"
        isMain = True
        for prop in relicList:
            if isMain:
                Utils._content['relic_content'] += f"<div class=relicPropContainer><p><span class=important style=color:#d97d22;background-color:#40405f;font-size:14px><strong>{prop}</strong></span></p>"
                isMain = False
            else:
                Utils._content['relic_content'] += f"<p>{prop}</p>"
        Utils._content['relic_content'] += "</div></div>"
        time.sleep(1)
        if auto.click_element("./assets/images/fight/relic_lock.png", "image", 0.9, max_retries=5):
            logger.info(gu("胚子已锁定"))
            time.sleep(1)
        return
    
    def rubbish_relic():
        logger.info(gu("鉴定为垃圾"))
        if auto.click_element("./assets/images/fight/relic_rubbish.png", "image", 0.9, max_retries=5):
            logger.info(gu("已标记为垃圾"))
            time.sleep(1)
        return
    
    @staticmethod
    def is_good_relic(relicName, relicPart, relicList, propCount, usefulPropCount, mainPropName):
        logger.info(gu("开始检测遗器"))
        if (propCount >= 3 and usefulPropCount == 2):
            if relicPart in ['头部', '手部']:
                logger.warning(gu(f"发现头部/手部胚子"))
            elif relicPart in '躯干':
                logger.warning(gu(f"发现躯干胚子"))
            elif relicPart in '脚部':
                logger.warning(gu(f"发现脚部胚子"))
            elif relicPart in '位面球':
                logger.warning(gu(f"发现位面球胚子"))
            elif relicPart in '连结绳':
                logger.warning(gu(f"发现连结绳胚子"))

            Relics.create_relic_content(relicName, relicPart, relicList)

        elif (propCount == 3 and usefulPropCount == 1):
            if relicPart in ['头部', '手部']:
                logger.warning(gu(f"发现头部/手部胚子"))
                Relics.create_relic_content(relicName, relicPart, relicList)

            elif relicPart in '躯干' and mainPropName in ['暴击率','暴击伤害','攻击力']:
                logger.warning(gu(f"发现躯干胚子"))
                Relics.create_relic_content(relicName, relicPart, relicList)

            elif relicPart in '脚部' and mainPropName in ['速度','攻击力']:
                logger.warning(gu(f"发现脚部胚子"))
                Relics.create_relic_content(relicName, relicPart, relicList)

            elif relicPart in '位面球' and mainPropName in ['量子属性伤害加成','风属性伤害加成','火属性伤害加成','雷属性伤害加成','冰属性伤害加成','虚数属性伤害加成','攻击力']:
                logger.warning(gu(f"发现位面球胚子"))
                Relics.create_relic_content(relicName, relicPart, relicList)

            elif relicPart in '连结绳' and mainPropName not in ['防御力']:
                logger.warning(gu(f"发现连结绳胚子"))
                Relics.create_relic_content(relicName, relicPart, relicList)
        elif (propCount == 3 and usefulPropCount == 0):
            if relicPart in '躯干' and mainPropName in ['暴击率','暴击伤害']:
                logger.warning(gu(f"发现躯干胚子"))
                Relics.create_relic_content(relicName, relicPart, relicList)
            else:
                Relics.rubbish_relic()
        elif propCount == 4 and usefulPropCount == 0:
            Relics.rubbish_relic()
                

    @staticmethod
    def instance_get_relic():
        relic_name_crop=(783.0 / 1920, 318.0 / 1080, 436.0 / 1920, 53.0 / 1080) # 遗器名称
        relic_prop_crop=(831.0 / 1920, 398.0 / 1080, 651.0 / 1920, 181.0 / 1080) # 遗器属性
        logger.info(gu("开始检测遗器"))

        point = auto.find_element("./assets/images/fight/fight_reward.png", "image", 0.9, max_retries=2)
        
        success_reward_top_left_x = point[0][0]
        success_reward_top_left_y = point[0][1]

        for i in range(2):
            for j in range(7):

                auto.click_element_with_pos(((success_reward_top_left_x -380 + j *120, success_reward_top_left_y + 40 + i * 120), (success_reward_top_left_x -380 + 120 + j *120, success_reward_top_left_y + 40 + 120 + i * 120)))
                    
                if not auto.find_element("./assets/images/fight/5star.png", "image", 0.9, max_retries=2):
                    if auto.click_element("./assets/images/fight/relic_info_close.png", "image", 0.9, max_retries=3):
                        time.sleep(0.5)
                    else:
                        break
                else:
                    time.sleep(0.5)
                    relic_name = auto.get_single_line_text(relic_name_crop, blacklist=[], max_retries=5)

                    relic_part = auto.get_single_line_text(crop=(515.0 / 1920, 726.0 / 1080, 91.0 / 1920, 35.0 / 1080),blacklist=['+','0'],max_retries=3)
                    logger.info(gu(f"{relic_name}:{relic_part}"))

                    auto.take_screenshot(crop=relic_prop_crop)
                    time.sleep(0.5)
                    
                    isProp = False
                    tempMainPropName = ''
                    propCount = -1
                    usefulPropCount = 0
                    relicList = list()
                    isMainProp = True

                    result = ocr.recognize_multi_lines(auto.screenshot)
                    time.sleep(0.5)

                    tempListValue = ''

                    for box in result:
                        text = box[1][0]
                        if text in ['暴击率','暴击伤害','生命值','攻击力','防御力','能量恢复效率','效果命中','效果抵抗','速度','击破特攻','治疗量加成','量子属性伤害加成','风属性伤害加成','火属性伤害加成','雷属性伤害加成','冰属性伤害加成','虚数属性伤害加成']:
                            if isMainProp:
                                tempMainPropName = text
                            tempListValue = f'{text}:'
                            isProp = True
                            if text in ['暴击率','暴击伤害']:
                                usefulPropCount += 1
                            continue
                        elif isProp:
                            if isMainProp:
                                isMainProp = False
                            # tempPropValue = text
                            tempListValue += f'{text}'
                            isProp = False
                            propCount += 1
                        else:
                            continue
                        # logger.info(f"{tempListValue}")
                        relicList.append(tempListValue)
                    
                    # logger.info(f"{propCount}")
                    # logger.info(f"{usefulPropCount}")
                    allPropText = '词条:'
                    for key in relicList:
                        allPropText += f'{key},'
                    logger.info(gu(allPropText))
                    logger.info(gu(f"总词条数:{propCount},有效词条:{usefulPropCount}"))

                    Relics.is_good_relic(relic_name, relic_part, relicList, propCount, usefulPropCount, tempMainPropName)
                    
                    time.sleep(0.5)
                    if auto.click_element("./assets/images/fight/relic_info_close.png", "image", 0.9, max_retries=3):
                        time.sleep(0.5)
