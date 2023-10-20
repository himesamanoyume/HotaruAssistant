from managers.config_manager import config
from managers.logger_manager import logger
from managers.automation_manager import auto
from managers.translate_manager import _

class Utils:
    uid = None
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
    
    def get_uid(crop):
        try:
            uid = auto.get_single_line_text(crop=crop, blacklist=[], max_retries=9)
            logger.info(_(f"识别到UID为:{uid}"))
            return uid
        except Exception as e:
            logger.error(_("识别UID失败: {error}").format(error=e))
            return -1