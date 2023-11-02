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
import time


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
        elif not os.path.exists(os.path.join(config.universe_path, 'gui.exe')):
            logger.error(_("模拟宇宙缺失核心文件，请尝试更新"))
            return False
        # 日常任务需要能够自定义次数的模拟宇宙版本，检测是否存在 nums 参数
        with open(os.path.join(config.universe_path, 'states.py'), 'r', encoding='utf-8') as f:
            if "nums" not in f.read():
                logger.warning(_("模拟宇宙版本过低"))
                Universe.update()
        return True

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
        check_result = True
        PythonChecker.run()
        check_result &= Universe.check_path()
        Universe.check_requirements()
        return check_result
    

    @staticmethod
    def start(get_reward=False, nums=config.universe_count, save=True, daily=True):
        logger.hr(_("准备模拟宇宙"), 2)
        Utils.detectIsNoneButNoSave(config.universe_fin, Utils.get_uid(), False)
        config.save_config()
        if config.universe_fin[Utils.get_uid()] and daily:
            logger.info(_("鉴定为正在每日任务中且分数已满,跳过"))
            return True
        if Universe.before_start():
            command = [config.python_exe_path, "states.py"]
            screen.change_to('main')

            logger.info(_("开始校准"))
            if subprocess_with_timeout([config.python_exe_path, "align_angle.py"], 60, config.universe_path, config.env):
                
                screen.change_to('universe_main')
                logger.info(_("开始模拟宇宙"))
                config._load_config()
                # for循环2次,每次开始时都检测一遍积分
                for i in range(2):
                    time.sleep(0.5)
                    # 如果一开始就能检测到积分奖励画面 说明是每周第一次进入界面刷新时
                    if auto.find_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10):
                        current_score, max_score = Utils.get_universe_score()
                        auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10)

                    elif auto.click_element("./assets/images/universe/universe_reward.png", "image", 0.9):
                        time.sleep(1)
                        current_score, max_score = Utils.get_universe_score()
                        if auto.click_element("./assets/images/universe/one_key_receive.png", "image", 0.9, max_retries=10):
                            time.sleep(0.5)
                            if auto.find_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10):
                                time.sleep(0.5)
                                logger.info(_("🎉模拟宇宙积分奖励已领取🎉"))
                                # Base.send_notification_with_screenshot(_("🎉模拟宇宙积分奖励已领取🎉"))
                                auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10)
                    
                    time.sleep(0.5)
                    screen.change_to('universe_main')
                    
                    # 若为0,则设置bonus=0,则既不为0也不为最大积分,则bonus=1,若为最大积分,则只根据universe_bonus_enable决定是否领取
                    if current_score == 0:
                        logger.info(_("积分为0,鉴定为首次进行模拟宇宙,本次将不领取沉浸奖励"))
                        command.append("--bonus=0")
                        command.append("--nums=1")
                    elif current_score == max_score:
                        logger.info(_("积分为最大积分,鉴定为完成周常后额外进行模拟宇宙,本次将根据config决定是否领取沉浸奖励"))
                        if daily:
                            logger.info(_("鉴定为正在每日任务中,最大积分情况下将直接跳过"))
                            return False
                        if config.universe_bonus_enable:
                            command.append("--bonus=1")
                        if nums:
                            command.append(f"--nums={nums}")
                    else:
                        logger.info(_("积分不为0也不为最大积分,鉴定为不是首次进行模拟宇宙,本次将领取沉浸奖励"))
                        command.append("--bonus=1")
                        command.append("--nums=1")
                    # end
                    logger.info(_("将开始第{index}次进行模拟宇宙").format(index=i+1))
                    if subprocess_with_timeout(command, config.universe_timeout * 3600, config.universe_path, config.env):
                    
                        screen.change_to('main')
                        # 此时保存运行的时间戳
                        if save:
                            Utils.saveTimestamp('universe_timestamp', Utils.get_uid())
                        # end

                        if get_reward:
                            # 此时领取积分奖励
                            Universe.get_reward()
                            # end
                        else:
                            # 改成第一/二次模拟宇宙已完成
                            logger.info(_("🎉第{index}次模拟宇宙已完成🎉").format(index=i+1))
                            Utils._temp += "<p>"+f'模拟宇宙已完成{i+1}次</p>'

                            # end
                        return True
                    else:
                        logger.error(_("模拟宇宙失败"))
                    # end
            else:
                logger.error(_("校准失败"))
        logger.warning(_("⚠️模拟宇宙未完成⚠️"))
        return False

    @staticmethod
    def get_reward():
        logger.info(_("开始领取模拟宇宙积分奖励"))
        screen.change_to('universe_main')
        time.sleep(0.5)
        if auto.click_element("./assets/images/universe/universe_reward.png", "image", 0.9):
            time.sleep(0.5)
            if auto.click_element("./assets/images/universe/one_key_receive.png", "image", 0.9, max_retries=10):
                time.sleep(0.5)
                if auto.find_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10):
                    time.sleep(0.5)
                    Utils.get_universe_score()
                    logger.info(_("🎉模拟宇宙积分奖励已领取🎉"))
                    # Base.send_notification_with_screenshot(_("🎉模拟宇宙积分奖励已领取🎉"))
                    auto.click_element("./assets/images/base/click_close.png", "image", 0.9, max_retries=10)
        time.sleep(0.5)
        screen.change_to('universe_main')
        time.sleep(0.5)

    @staticmethod
    def gui():
        if Universe.before_start():
            if subprocess.run(["start", "gui.exe"], shell=True, check=True, cwd=config.universe_path, env=config.env):
                return True
        return False
