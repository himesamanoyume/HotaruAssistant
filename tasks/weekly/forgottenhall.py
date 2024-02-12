from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.config_manager import config
from managers.logger_manager import logger
from managers.translate_manager import _
from managers.utils_manager import gu
from tasks.daily.utils import Utils
import time


class ForgottenHall:
    def get_star_and_level():
        screen.change_to('guide4')
        # guide4_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        guide4_little_crop=(250.0 / 1920, 413.0 / 1080, 432.0 / 1920, 488.0 / 1080)
        # little_crop指第一行不在范围内的坐标
        if auto.click_element("忘却之庭", "text", max_retries=20, crop=guide4_little_crop):
            time.sleep(1)
            countdownTextCrop=(1484.0 / 1920, 556.0 / 1080, 135.0 / 1920, 27.0 / 1080)
            levelTextCrop=(1312.0 / 1920, 641.0 / 1080, 95.0 / 1920, 31.0 / 1080)
            starTextCrop=(1309.0 / 1920, 682.0 / 1080, 102.0 / 1920, 33.0 / 1080)
            try:
                time.sleep(0.5)
                countdownText = auto.get_single_line_text(crop=countdownTextCrop, blacklist=[], max_retries=6)
                countdownText = countdownText.replace('）','').replace(')','').replace('①','').replace('?','')
                if countdownText == '?':
                    countdownText = '识别出错'
                levelText = auto.get_single_line_text(crop=levelTextCrop, blacklist=[], max_retries=3)
                starText = auto.get_single_line_text(crop=starTextCrop, blacklist=[], max_retries=3)
                logger.info(gu(f"忘却之庭刷新倒计时:{countdownText},层数:{levelText},星数:{starText}"))
                Utils._content['fh_countdownText'] = countdownText
                level = levelText.split('/')[0]
                star = starText.split('/')[0]
                config.forgottenhall_levels[Utils.get_uid()] = int(level)
                config.forgottenhall_stars[Utils.get_uid()] = int(star)
                config.save_config()
            except Exception as e:
                nowtime = time.time()
                logger.error(gu(f"{nowtime},识别忘却之庭失败:{e}"))
                raise Exception(f"{nowtime},识别忘却之庭失败:{e}")

        # screen.change_to('menu')
        return True