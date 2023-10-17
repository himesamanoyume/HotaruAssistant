from managers.config_manager import config
from managers.logger_manager import logger
from managers.translate_manager import _

class Utils:
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