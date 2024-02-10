from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.logger_manager import logger
from managers.utils_manager import gu
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
