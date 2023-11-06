from managers.logger_manager import logger
from managers.screen_manager import screen
from managers.automation_manager import auto
from managers.translate_manager import _
from managers.config_manager import config
from managers.notify_manager import notify
from tasks.daily.utils import Utils
from datetime import datetime
from tasks.game.start import Start
from tasks.game.stop import Stop
import sys


class Game:
    @staticmethod
    def start():
        logger.hr(_("开始运行"), 0)
        logger.info(_("开始启动游戏"))
        if not auto.retry_with_timeout(lambda: Start.start_game(), 1200, 1):
            # notify.notify(_("⚠️启动游戏超时，退出程序⚠️"))
            logger.error(_("⚠️启动游戏超时，退出程序⚠️"))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)
        # 判断手机壁纸
        screen.change_to('menu')
        if not auto.find_element("./assets/images/menu/journey.png", "image", 0.8):
            logger.info(_("检测到未使用无名路途壁纸"))
            screen.change_to('wallpaper')
            if auto.click_element("./assets/images/menu/wallpaper/journey.png", "image", 0.8):
                auto.click_element("更换", "text", max_retries=4)
            auto.press_key("esc")
            logger.info(_("更换到无名路途壁纸成功"))
        logger.hr(_("完成"), 2)

    @staticmethod
    def stop(index, detect_loop=False):
        Utils._content.update({'date':f'{datetime.now()}'})
        i =0
        for task_name, task_value in config.daily_tasks[Utils.get_uid()].items():
            Utils._content.update({f'daily_0{i}':f'{task_name}'})
            Utils._content.update({f'daily_0{i}_value':task_value})
            i+=1

        scoreAndMaxScore = config.universe_score[Utils.get_uid()]

        current_score = scoreAndMaxScore.split('/')[0]
        max_score = scoreAndMaxScore.split('/')[1]
        Utils._content.update({'current_universe_score':f'{current_score}'})
        Utils._content.update({'max_universe_score':f'{max_score}'})

        Utils._content.update({'daily_tasks_score':f'{config.daily_tasks_score[Utils.get_uid()]}'})
        Utils._content.update({'multi_content':f"{Utils._temp}"})

        notify.notify(_(f'UID:{Utils.get_uid()},上号刚刚结束!'), _("普罗丢瑟代练"))

        if config.multi_login:
            logger.hr(_("多账号结束运行一个账号"), 0)
            if index == len(config.multi_login_accounts) - 1:
                logger.hr(_("停止运行"), 0)
                # Stop.play_audio()
                if detect_loop and config.after_finish == "Loop":
                    Stop.after_finish_is_loop()
                else:
                    Stop.after_finish_not_loop()
            else:
                Stop.stop_game()
        else:
            logger.hr(_("单账号停止运行"), 0)
            Stop.play_audio()
            if detect_loop and config.after_finish == "Loop":
                Stop.after_finish_is_loop()
            else:
                Stop.after_finish_not_loop()
