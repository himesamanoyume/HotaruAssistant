from managers.screen_manager import screen
from managers.config_manager import config
from managers.logger_manager import logger
from managers.automation_manager import auto
from managers.translate_manager import _
from tasks.base.base import Base
from tasks.base.pythonchecker import PythonChecker
from tasks.daily.utils import Utils
from tasks.base.command import subprocess_with_timeout
import subprocess
import os


class Universe:
    @staticmethod
    def update():
        config.set_value("universe_requirements", False)
        from module.update.update_handler import UpdateHandler
        from tasks.base.fastest_mirror import FastestMirror
        url = FastestMirror.get_github_mirror("https://github.com/CHNZYX/Auto_Simulated_Universe/archive/main.zip")
        update_handler = UpdateHandler(url, config.universe_path, "Auto_Simulated_Universe-main")
        update_handler.run()

    @staticmethod
    def check_path():
        if not os.path.exists(config.universe_path):
            logger.warning(_("模拟宇宙路径不存在: {path}").format(path=config.universe_path))
            Universe.update()

    @staticmethod
    def check_requirements():
        if not config.universe_requirements:
            logger.info(_("开始安装依赖"))
            from tasks.base.fastest_mirror import FastestMirror
            subprocess.run([config.python_exe_path, "-m", "pip", "install", "-i", FastestMirror.get_pypi_mirror(), "pip", "--upgrade"])
            while not subprocess.run([config.python_exe_path, "-m", "pip", "install", "-i", FastestMirror.get_pypi_mirror(), "-r", "requirements.txt"], check=True, cwd=config.universe_path):
                logger.error(_("依赖安装失败"))
                input(_("按回车键重试. . ."))
            logger.info(_("依赖安装成功"))
            config.set_value("universe_requirements", True)

    @staticmethod
    def before_start():
        PythonChecker.run()
        Universe.check_path()
        Universe.check_requirements()
        return True

    @staticmethod
    def start(get_reward=False):
        logger.hr(_("准备模拟宇宙"), 2)

        if Universe.before_start():
            screen.change_to('main')
            logger.info(_("开始校准"))
            if subprocess_with_timeout([config.python_exe_path, "align_angle.py"], 60, config.universe_path, config.env):
                screen.change_to('universe_main')
                logger.info(_("开始模拟宇宙"))
                # 判断第一次运行的时间戳是否为上周

                # end
                # 若此时为新的一周，则开始第一次模拟宇宙,bonus=0
                command = [config.python_exe_path, "states.py"]
                if config.universe_bonus_enable:
                    command.append("--bonus=0")
                # end
                if subprocess_with_timeout(command, config.universe_timeout * 3600, config.universe_path, config.env):
                    
                    # 此时保存为第一次运行的时间戳
                    Utils.saveTimestamp('universe_timestamp', Utils.get_uid())
                    # end

                    if get_reward:
                        # 此时领取7500奖励
                        Universe.get_reward()
                        # end
                    else:
                        # 改成第一次模拟宇宙已完成
                        Base.send_notification_with_screenshot(_("🎉模拟宇宙已完成🎉"))
                        # end
                    return
                else:
                    logger.error(_("模拟宇宙失败"))

                # 判断第二次运行的时间戳是否为上周

                # end
                # 若此时为新的一周，则开始第二次模拟宇宙,bonus=1
                command = [config.python_exe_path, "states.py"]
                if config.universe_bonus_enable:
                    command.append("--bonus=1")
                # end
                # 保证第二次运行时领取沉浸奖励的成功
                if subprocess_with_timeout(command, config.universe_timeout * 3600, config.universe_path, config.env):
                # end
                
                    # 此时保存为第二次运行的时间戳
                    Utils.saveTimestamp('universe_timestamp', Utils.get_uid())
                    # end

                    if get_reward:
                        # 此时领取15000奖励
                        Universe.get_reward()
                        # end
                    else:
                        # 改成第二次模拟宇宙已完成
                        Base.send_notification_with_screenshot(_("🎉模拟宇宙已完成🎉"))
                        # end
                    return
                else:
                    logger.error(_("模拟宇宙失败"))
            else:
                logger.error(_("校准失败"))
        Base.send_notification_with_screenshot(_("⚠️模拟宇宙未完成⚠️"))

    @staticmethod
    def get_reward():
        logger.info(_("开始领取奖励"))
        screen.change_to('universe_main')
        if auto.click_element("./assets/images/universe/universe_reward.png", "image", 0.9):
            if auto.click_element("./assets/images/universe/one_key_receive.png", "image", 0.9, max_retries=10):
                if auto.find_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10):
                    Base.send_notification_with_screenshot(_("🎉模拟宇宙奖励已领取🎉"))
                    auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10)

    @staticmethod
    def gui():
        if Universe.before_start():
            if subprocess.run(["start", "gui.exe"], shell=True, check=True, cwd=config.universe_path, env=config.env):
                return True
        return False
