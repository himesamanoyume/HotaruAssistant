from managers.config_manager import config
from managers.logger_manager import logger
from managers.automation_manager import auto
from tasks.base.date import Date
from managers.translate_manager import _

class Utils:
    _uid = '-1'
    def detectTimestamp(timestamp, uid):
        if timestamp == {}:
            timestamp[uid] = 0
            config.save_config()

        if uid not in timestamp.keys():
            timestamp[uid] = 0
            config.save_config()

    def saveTimestamp(timestamp, uid):
        if config.save_timestamp(timestamp, uid):
            logger.info(_("已更新时间戳"))
        else:
            logger.info(_("更新时间戳出错"))

    def saveConfigByUid():
        return
    
    def get_universe_score():
        max_crop = (298.0 / 1920, 924.0 / 1080, 91.0 / 1920, 40.0 / 1080)
        current_crop = (154.0 / 1920, 912.0 / 1080, 134.0 / 1920, 48.0 / 1080)
        try:
            max_score = auto.get_single_line_text(crop=max_crop, blacklist=[], max_retries=5)
            current_score = auto.get_single_line_text(crop=current_crop, blacklist=[], max_retries=5)
            logger.info(_(f"识别到当前积分为:{max_score}"))
            logger.info(_(f"识别到积分上限为:{current_score}"))
            return int(current_score), int(max_score)
        except Exception as e:
            logger.error(_("识别模拟宇宙积分失败: {error}").format(error=e))
            logger.warning(_("因读取模拟宇宙积分失败,程序中止"))

    
    def get_new_uid():
        uid_crop = (68.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080)
        try:
            Utils._uid = auto.get_single_line_text(crop=uid_crop, blacklist=[], max_retries=9)
            logger.info(_(f"识别到UID为:{Utils._uid}"))
        except Exception as e:
            logger.error(_("识别UID失败: {error}").format(error=e))
            logger.warning(_("因读取UID失败,程序中止"))
        
    def get_uid():
        if Utils._uid == '-1':
            Utils.get_new_uid()
            return Utils._uid
        else:
            return Utils._uid
        
    def is_next_4_am(timestamp, uid):
        Utils.detectTimestamp(timestamp, uid)
        return Date.is_next_4_am(timestamp[uid])
    
    def is_next_mon_4_am(timestamp, uid):
        Utils.detectTimestamp(timestamp, uid)
        return Date.is_next_mon_4_am(timestamp[uid])