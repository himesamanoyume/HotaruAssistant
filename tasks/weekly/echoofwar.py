from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.config_manager import config
from managers.logger_manager import logger
from managers.translate_manager import _
from managers.utils_manager import gu
from tasks.daily.utils import Utils
from tasks.power.power import Power
from module.automation.screenshot import Screenshot
from tasks.daily.relics import Relics
import time


class Echoofwar:
    @staticmethod
    def echoofwar_get_times():
        screen.change_to('guide3')
        guide3_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        if auto.click_element("侵蚀隧洞", "text", max_retries=10, crop=guide3_crop):
            auto.mouse_scroll(12, -1)
            if auto.click_element("历战余响", "text", max_retries=10, crop=guide3_crop):
                auto.find_element("历战余响", "text", max_retries=10, crop=(
                    682.0 / 1920, 275.0 / 1080, 1002.0 / 1920, 184.0 / 1080), include=True)
                for box in auto.ocr_result:
                    text = box[1][0]
                    if "/3" in text:
                        logger.info(gu(f"历战余响本周可领取奖励次数：{text}"))
                        reward_count = int(text.split("/")[0])

                        config.echo_of_war_times[Utils.get_uid()] = reward_count
                        config.save_config()

    @staticmethod
    def start():
        Relics.detect_relic_count()
        if Utils._relicCount >= 1450:
            nowtime = time.time()
            logger.error(gu(f"{nowtime},检测到遗器数量超过1450,所有可能获得遗器的副本全部跳过,出现该致命错误意味着你没有选择开启遗器自动分解开关,若不打算开启,则只能自行上号清理,否则每次上号时遗器数量超标时都会直接中止"))
            raise Exception(f"{nowtime},检测到遗器数量超过1450,所有可能获得遗器的副本全部跳过,出现该致命错误意味着你没有选择开启遗器自动分解开关,若不打算开启,则只能自行上号清理,否则每次上号时遗器数量超标时都会直接中止")
        try:
            logger.hr(_("准备历战余响"), 2)
            screen.change_to('guide3')
            guide3_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
            if auto.click_element("侵蚀隧洞", "text", max_retries=10, crop=guide3_crop):
                auto.mouse_scroll(12, -1)
                if auto.click_element("历战余响", "text", max_retries=10, crop=guide3_crop):
                    auto.find_element("历战余响", "text", max_retries=10, crop=(
                        682.0 / 1920, 275.0 / 1080, 1002.0 / 1920, 184.0 / 1080), include=True)
                    for box in auto.ocr_result:
                        text = box[1][0]
                        if "/3" in text:
                            logger.info(gu(f"历战余响本周可领取奖励次数：{text}"))
                            reward_count = int(text.split("/")[0])

                            config.echo_of_war_times[Utils.get_uid()] = reward_count
                            config.save_config()
                            
                            if reward_count == 0:
                                logger.info(gu("历战余响已完成"))
                                # config.save_timestamp("echo_of_war_timestamp")

                                Utils.saveTimestamp('echo_of_war_timestamp', Utils.get_uid())

                                screen.change_to('menu')
                                return True
                            else:
                                power = Power.power()
                                max_count = power // 30
                                if max_count == 0:
                                    logger.info(gu("🟣开拓力 < 30"))
                                    return
                                elif reward_count <= max_count:
                                    Utils.saveTimestamp('echo_of_war_timestamp', Utils.get_uid())

                                return Power.run_instances("历战余响", config.instance_names[Utils.get_uid()]["历战余响"], 30, min(reward_count, max_count))
            return False
        except Exception as e:
            logger.error(gu(f"历战余响失败: {e}"))
            return False
