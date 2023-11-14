from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.logger_manager import logger
from managers.config_manager import config
from managers.translate_manager import _
from tasks.daily.utils import Utils
import time

class Relics:
    @staticmethod
    def salvage():
        try:
            logger.hr(_("准备分解遗器"), 2)
            # screen.get_current_screen()
            if not config.relic_salvage_enable[Utils.get_uid()]:
                logger.info("检测到分解遗器未开启,跳过分解遗器")
                return
            screen.change_to('bag_relics')
            if auto.click_element("分解", "text", max_retries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                if auto.click_element("分解", "text", max_retries=10, crop=(1156.0 / 1920, 959.0 / 1080, 199.0 / 1920, 59.0 / 1080)):
                    time.sleep(1)
                    if auto.click_element("./assets/images/synthesis/filter.png", "image", 0.9, max_retries=10):
                        # 等待筛选界面弹出
                        time.sleep(1)
                        auto.click_element("2星", "text", max_retries=10, crop=(1408.0 / 1920, 308.0 / 1080, 336.0 / 1920, 136.0 / 1080))
                        time.sleep(0.5)
                        auto.click_element("3星", "text", max_retries=10, crop=(1408.0 / 1920, 308.0 / 1080, 336.0 / 1920, 136.0 / 1080))
                        time.sleep(0.5)
                        auto.click_element("4星", "text", max_retries=10, crop=(1408.0 / 1920, 308.0 / 1080, 336.0 / 1920, 136.0 / 1080))
                        time.sleep(0.5)
                        if auto.click_element("确认", "text", max_retries=10, crop=(1597.0 / 1920, 958.0 / 1080, 285.0 / 1920, 65.0 / 1080)):
                            time.sleep(1)
                            if auto.click_element("全选", "text", max_retries=10, crop=(937.0 / 1920, 951.0 / 1080, 121.0 / 1920, 63.0 / 1080)):
                                time.sleep(5)
                                if auto.find_element("./assets/images/screen/bag/all_select.png", "image", 0.9, max_retries=10):
                                    countText = auto.get_single_line_text((616.0 / 1920, 871.0 / 1080, 110.0 / 1920, 37.0 / 1080), [], 5)
                                    count = countText.split('/')[0]
                                    logger.info(f"已选数量:{count}/500")
                                    if auto.click_element("分解", "text", max_retries=10, crop=(1597.0 / 1920, 958.0 / 1080, 285.0 / 1920, 65.0 / 1080)):
                                        time.sleep(1)
                                        if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=10):
                                            time.sleep(1)
                                            if auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10):
                                                time.sleep(1)
                                                logger.info(_(f"分解遗器{count}件完成"))
                                                screen.change_to('main')
                                                return True
                                else:
                                    logger.error(_("分解遗器失败: 没有多余的遗器可供分解"))
                                    screen.change_to('main')
                                    return False
            logger.error(_("分解遗器失败"))
            return False
        except Exception as e:
            logger.error(_("分解遗器失败: {error}").format(error=e))
        return False
    
    @staticmethod
    def detect_relic_count():
        try:
            logger.hr(_("准备检测遗器数量"), 2)
            # screen.get_current_screen()
            screen.change_to('bag_relics')
            relic_count_crop=(1021.0 / 1920, 974.0 / 1080, 131.0 / 1920, 33.0 / 1080)
            relic_countText = auto.get_single_line_text(relic_count_crop, ['遗','器','数','量'], max_retries=5)
            logger.info(f"遗器数量:{relic_countText}")
            relic_countText = relic_countText.split('/')[0]
            Utils._relicCount = int(relic_countText)
            if Utils._relicCount >= 1450:
                logger.warning("检测到遗器数量超标")
                Relics.salvage()
                Relics.detect_relic_count()

        except Exception as e:
            logger.error(_("检测遗器数量失败: {error}").format(error=e))
        return False
