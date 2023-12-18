from tasks.base.fastest_mirror import FastestMirror
from managers.logger_manager import logger
from managers.translate_manager import _
from managers.config_manager import config
from managers.notify_manager import notify
from managers.utils_manager import gu
from packaging.version import parse
import requests
import json


class Version:
    @staticmethod
    def start():
        if not config.check_update:
            logger.debug(gu("检测更新未开启"))
            return False
        logger.hr(gu("开始检测更新"), 0)
        try:
            response = requests.get(FastestMirror.get_github_api_mirror("himesamanoyume","himesamanoyume","latest.json",1), timeout=3)
            if response.status_code == 200:
                data = json.loads(response.text)
                version = data["tag_name"]
                logger.info(gu(f"最新版本:{version},当前版本:{config.version}"))
                if parse(version.lstrip('v')) > parse(config.version.lstrip('v')):
                    logger.info(gu(f"发现新版本,请退出程序使用Update.exe进行更新"))
                    logger.info(data["html_url"])
                else:
                    logger.info(gu("已经是最新版本"))
            else:
                logger.warning(gu("检测更新失败"))
                logger.debug(response.text)
        except Exception as e:
            logger.warning(gu("检测更新失败"))
            logger.debug(e)
        logger.hr(gu("完成"), 2)
