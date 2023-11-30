from managers.logger_manager import logger
from managers.automation_manager import auto
from managers.translate_manager import _
from managers.config_manager import config
from managers.utils_manager import gu
from managers.notify_manager import notify
from managers.ocr_manager import ocr
from tasks.power.power import Power
from tasks.daily.utils import Utils
from tasks.base.date import Date
from tasks.base.windowswitcher import WindowSwitcher
import psutil
import random
import time
import sys
import os


class Stop:
    @staticmethod
    def terminate_process(name, timeout=10):
        # 根据进程名中止进程
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if name in proc.info['name']:
                try:
                    process = psutil.Process(proc.info['pid'])
                    process.terminate()
                    process.wait(timeout)
                    return True
                except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied):
                    pass
        return False
    
    @staticmethod
    def altF4_process():
        # 确定为对应游戏窗口后alt+f4
        return

    @staticmethod
    def stop_game():
        import pyautogui
        logger.info(gu("开始退出游戏"))
        time.sleep(2)
        if WindowSwitcher.check_and_switch(config.game_title_name):
            # if not auto.retry_with_timeout(lambda: Stop.terminate_process(config.game_process_name), 10, 1):
            #     logger.error(_("游戏退出失败"))
            #     return False
            time.sleep(1)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(5)
            # 新增检查是否还在的判断
            if not WindowSwitcher.check_and_switch(config.game_title_name):
                logger.info(gu("游戏退出成功"))
            else:
                pyautogui.hotkey('alt', 'f4')
                time.sleep(5)
                if WindowSwitcher.check_and_switch(config.game_title_name):
                    auto.retry_with_timeout(lambda: Stop.terminate_process(config.game_process_name), 10, 1)
            Utils._uid = "-1"
            # end
        else:
            logger.warning(_("游戏已经退出了"))
        return True

    @staticmethod
    def get_wait_time(current_power):
        # 距离体力到达配置文件指定的上限剩余秒数
        wait_time_power_limit = (config.power_limit - current_power) * 6 * 60
        # 距离第二天凌晨4点剩余秒数，+30避免显示3点59分不美观，#7
        wait_time_next_day = Date.get_time_next_4am() + random.randint(30, 600)
        # 取最小值
        wait_time = min(wait_time_power_limit, wait_time_next_day)
        return wait_time
    
    @staticmethod
    def get_wait_time_with_total_time(total_time):
        # 距离体力到达配置文件指定的上限剩余秒数
        wait_time = 12 * 3600 - total_time
        if wait_time < 0:
            wait_time = 0
        # 距离第二天凌晨4点剩余秒数，+30避免显示3点59分不美观，#7
        wait_time_next_day = Date.get_time_next_4am() + random.randint(30, 600)
        # 取最小值
        wait_time = min(wait_time, wait_time_next_day)
        return wait_time

    @staticmethod
    def play_audio():
        if config.play_audio:
            logger.debug(_("开始播放音频"))
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
            import pygame.mixer

            pygame.init()
            pygame.mixer.music.load('./assets/audio/pa.mp3')
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            logger.debug(_("播放音频完成"))

    @staticmethod
    def shutdown():
        logger.warning(_("将在{num}分钟后自动关机").format(num=1))
        time.sleep(60)
        os.system("shutdown /s /t 0")

    @staticmethod
    def hibernate():
        logger.warning(_("将在{num}分钟后自动休眠").format(num=1))
        time.sleep(60)
        os.system("shutdown /h")

    @staticmethod
    def sleep():
        logger.warning(_("将在{num}分钟后自动睡眠").format(num=1))
        time.sleep(60)
        os.system("powercfg -h off")
        # 必须先关闭休眠，否则下面的指令不会进入睡眠，而是优先休眠，无语了，Windows为什么这么难用
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        os.system("powercfg -h on")

    @staticmethod
    def after_finish_is_loop():
        Stop.stop_game()
        # 等待状态退出OCR避免内存占用
        ocr.exit_ocr()
        logger.hr(gu("完成"), 2)
        total_time = time.time() - Utils._loop_start_timestamp

        wait_time = Stop.get_wait_time_with_total_time(total_time)
        future_time = Date.calculate_future_time(wait_time)
        logger.info(gu(f"将在{future_time}后继续运行"))

        time.sleep(wait_time)

    @staticmethod
    def after_finish_not_loop():
        if config.after_finish in ["Loop", "Shutdown", "Hibernate", "Sleep"]:
            if config.after_finish == "Shutdown":
                Stop.shutdown()
            elif config.after_finish == "Hibernate":
                Stop.hibernate()
            elif config.after_finish == "Sleep":
                Stop.sleep()
        elif config.after_finish in  ["Exit"]:
            Stop.stop_game()
            input(_("按回车键关闭窗口. . ."))
            sys.exit(0)
        logger.hr(gu("完成"), 2)

        # if config.after_finish not in ["Shutdown", "Hibernate", "Sleep"]:
        #     input(_("按回车键关闭窗口. . ."))
        # sys.exit(0)