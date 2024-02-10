from managers.screen_manager import screen
from managers.config_manager import config
from managers.logger_manager import logger
from managers.automation_manager import auto
from tasks.power.power import Power
from tasks.daily.relics import Relics
from managers.translate_manager import _
from managers.utils_manager import gu
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
        url = FastestMirror.get_github_mirror("https://github.com/himesamanoyume/Auto_Simulated_Universe/archive/main.zip")
        update_handler = UpdateHandler(url, config.universe_path, "Auto_Simulated_Universe-main")
        update_handler.run()

    @staticmethod
    def check_path():
        if not os.path.exists(config.universe_path):
            logger.warning(gu(f"模拟宇宙路径不存在: {config.universe_path}"))
            Universe.update()
        elif not os.path.exists(os.path.join(config.universe_path, 'gui.exe')):
            logger.error(gu("模拟宇宙缺失核心文件，请尝试更新"))
            return False
        # 日常任务需要能够自定义次数的模拟宇宙版本，检测是否存在 nums 参数
        with open(os.path.join(config.universe_path, 'states.py'), 'r', encoding='utf-8') as f:
            if "nums" not in f.read():
                logger.warning(gu("模拟宇宙版本过低"))
                Universe.update()
        return True

    @staticmethod
    def check_requirements():
        if not config.universe_requirements:
            logger.info(gu("开始安装依赖"))
            from tasks.base.fastest_mirror import FastestMirror
            subprocess.run([config.python_exe_path, "-m", "pip", "install", "-i", FastestMirror.get_pypi_mirror(), "pip", "--upgrade"])
            while not subprocess.run([config.python_exe_path, "-m", "pip", "install", "-i", FastestMirror.get_pypi_mirror(), "-r", "requirements.txt"], check=True, cwd=config.universe_path):
                logger.error(gu("依赖安装失败"))
                input(_("按回车键重试. . ."))
            logger.info(gu("依赖安装成功"))
            config.set_value("universe_requirements", True)

    @staticmethod
    def before_start():
        check_result = True
        PythonChecker.run()
        check_result &= Universe.check_path()
        Universe.check_requirements()
        return check_result
    

    @staticmethod
    def start(get_reward=False, nums=0, save=True, daily=True):
        Relics.detect_relic_count()
        Relics.skip_for_relic_count()
        
        logger.hr(gu("准备模拟宇宙"), 2)
        
        config.save_config()
        if config.universe_fin[Utils.get_uid()] and daily and not config.instance_type[Utils.get_uid()][0] == '模拟宇宙':
            logger.info(gu("鉴定为正在每日任务中且分数已满,跳过"))
            return True
        
        if Universe.before_start():
            
            screen.change_to('main')

            logger.info(gu("开始校准"))
            if subprocess_with_timeout([config.python_exe_path, "align_angle.py"], 60, config.universe_path, config.env):
                
                screen.change_to('universe_main')
                logger.info(gu("开始模拟宇宙"))

                # 使用nums时一般都是特殊需求使用来刷模拟宇宙
                if nums > 0:
                    for i in range(nums):
                        Universe.runUniverse(get_reward, save, daily)
                    return True
                else:
                    Universe.runUniverse(get_reward, save, daily)
                    return True
            else:
                logger.error(gu("校准失败"))
        
        logger.warning(gu("⚠️模拟宇宙未完成⚠️"))
        Power.power()
        return False
    
    @staticmethod
    def open_universe_score_screen():
        screen.change_to("universe_main")
        time.sleep(2)
        # 如果一开始就能检测到积分奖励画面 说明是每周第一次进入界面刷新时
        if auto.find_element("./assets/images/screen/universe/universe_score.png", "image", 0.9, max_retries=10):
            logger.info(gu("检测到模拟宇宙本周首次进入界面"))
            time.sleep(1)
            current_score, max_score = Utils.get_universe_score()
            auto.click_element("./assets/images/himeko/close.png", "image", 0.9, max_retries=10)

        elif auto.click_element("./assets/images/universe/universe_reward.png", "image", 0.9, max_retries=10):
            logger.info(gu("正在点开积分界面"))
            time.sleep(1)
            current_score, max_score = Utils.get_universe_score()
            if auto.click_element("./assets/images/universe/one_key_receive.png", "image", 0.9, max_retries=10):
                time.sleep(0.5)
                if auto.find_element("./assets/images/himeko/close.png", "image", 0.9, max_retries=10):
                    time.sleep(0.5)
                    logger.info(gu("🎉模拟宇宙积分奖励已领取🎉"))
                    # Base.send_notification_with_screenshot(_("🎉模拟宇宙积分奖励已领取🎉"))
                    auto.click_element("./assets/images/himeko/close.png", "image", 0.9, max_retries=10)
        
        return current_score, max_score
    
    @staticmethod
    def runUniverse(get_reward=False, save=True, daily=True):

        command = [config.python_exe_path, "states.py"]
        time.sleep(0.5)
        logger.info(gu("开始检测模拟宇宙积分"))
        current_score, max_score = Universe.open_universe_score_screen()
        Universe.get_immersifier()
        if not current_score < max_score:
            if (config.instance_type[Utils.get_uid()][0] == '模拟宇宙' and Utils._immersifiers < 4):
                logger.info(gu("鉴定为沉浸器数量不足,跳过"))
                return True
          
        time.sleep(0.5)

        if config.instance_type[Utils.get_uid()][0] == '模拟宇宙' or not config.universe_fin[Utils.get_uid()]:
            
            # if Utils._isFirstTimeSelectTeam:
            #     logger.info(gu("本账号首次运行模拟宇宙"))
            #     Utils._isFirstTimeSelectTeam = Universe.select_universe()
            # else:
            #     Universe.get_immersifier()
            Universe.select_universe()

            # screen.change_to('universe_main')
            # if current_score == None or max_score == None:
            #     current_score, max_score = Universe.open_universe_score_screen()

            # if not current_score < max_score:
            #     if (config.instance_type[Utils.get_uid()] == '模拟宇宙' and Utils._immersifiers <= 2):
            #         logger.info(gu("鉴定为沉浸器数量不足,跳过"))
            #         return True
            
            if current_score == 0:
                logger.info(gu("积分为0,鉴定为首次进行模拟宇宙"))
                if Utils._immersifiers > 0:
                    command.append("--bonus=1")
            elif current_score == max_score:
                logger.info(gu("积分为最大积分,鉴定为完成周常后额外进行模拟宇宙"))
                if Utils._immersifiers > 0:
                    command.append("--bonus=1")
                if daily and not config.instance_type[Utils.get_uid()][0] == '模拟宇宙':
                    logger.info(gu("鉴定为正在每日任务中,最大积分且清体力不为模拟宇宙的情况下将直接跳过"))
                    return False
            else:
                logger.info(gu("积分不为0也不为最大积分,鉴定为不是首次进行模拟宇宙"))
                command.append("--bonus=1")
            
            command.append(f"--nums=1")
                
            # end
            logger.info(gu("将开始进行模拟宇宙"))
            command.append(f"--fate={config.universe_fate[Utils.get_uid()]}")
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
                
                # Universe.get_immersifier()

                # if Utils._immersifiers > 0:
                #     logger.info("检测到沉浸器数量还有剩余,继续进行一次模拟宇宙")
                #     Universe.runUniverse(get_reward, save, daily)
                Universe.runUniverse(get_reward, save, daily)

                logger.info(gu("🎉模拟宇宙已完成1次🎉"))
                Utils._temp += f'<p>模拟宇宙已完成1次</p>'
                return True
            else:
                logger.error(gu("模拟宇宙失败"))
            # end

    @staticmethod
    def get_reward():
        logger.info(gu("开始领取模拟宇宙积分奖励"))
        Universe.open_universe_score_screen()
        screen.change_to('universe_main')

    @staticmethod
    def get_immersifier():
        Power.power()
        screen.change_to('guide3')
        instance_type_crop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        if config.instance_type[Utils.get_uid()][0] == '模拟宇宙':
            if Utils._power >= 40:
                count = Utils._power // 40
                logger.info(gu(f"开拓力能换{count}个沉浸器"))
                if auto.click_element("./assets/images/share/trailblaze_power/immersifiers.png", "image", 0.95, max_retries=10):
                    time.sleep(0.5)
                
                    for i in range(count-1):
                        auto.click_element("./assets/images/share/trailblaze_power/plus.png", "image", 0.9, max_retries=10)
                        time.sleep(0.5)

                    if auto.click_element("./assets/images/base/confirm.png", "image", 0.9, max_retries=10):
                        time.sleep(1)
                        auto.press_mouse()

        if not auto.click_element("模拟宇宙", "text", crop=instance_type_crop):
            if auto.click_element("凝滞虚影", "text", max_retries=10, crop=instance_type_crop):
                auto.mouse_scroll(12, 1)
                auto.click_element("模拟宇宙", "text", crop=instance_type_crop)

        time.sleep(0.5)
        try:
            result = auto.get_single_line_text(crop=(1673.0 / 1920, 50.0 / 1080, 71.0 / 1920, 31.0 / 1080),max_retries=5)
            count = result.split("/")[0]
            logger.info(gu(f"识别到沉浸器数量为:{count}"))
            Utils._immersifiers = int(count)
        except Exception as e:
            logger.error(gu(f"识别沉浸器数量失败: {e}"))
            Utils._immersifiers = 0

    @staticmethod
    def select_universe():

        # 截图过快会导致结果不可信
        time.sleep(1)

        # 传送
        instance_name_crop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
        auto.click_element("./assets/images/screen/guide/power.png", "image", max_retries=10)
        Flag = False
        match config.universe_number[Utils.get_uid()]:
            case 3:
                world_number = '第三世界'
            case 4:
                world_number = '第四世界'
            case 5:
                world_number = '第五世界'
            case 6:
                world_number = '第六世界'
            case 7:
                world_number = '第七世界'
            case _:
                world_number = '第三世界'
                Utils._content['universe_number'] = f"<blockquote style='background-color:#5f4040;box-shadow:3px 0 0 0 #d85959 inset;'><p>模拟宇宙难度选择有误,请告知我检查配置</p></blockquote>"

        for i in range(5):
            if auto.click_element("传送", "min_distance_text", crop=instance_name_crop, include=True, source=world_number):
                Flag = True
                break
            auto.mouse_scroll(20, -1)
            # 等待界面完全停止
            time.sleep(1)
        if not Flag:
            logger.error(gu("⚠️刷副本未完成 - 没有找到指定副本名称⚠️"))
            return False

        time.sleep(3)
        
        # 选择难度,0不是难度
        d = config.universe_difficulty[Utils.get_uid()]
        if not d in [1,2,3,4,5]:
            logger.warning(gu("难度设置不合法,进行难度5"))
            d = 5
        if config.universe_number[Utils.get_uid()] in [5,6,7] and d > 4:
            logger.warning(gu("第五、第六、第七世界暂不支持难度4以上,进行难度4"))
            d = 4
        
        # 用嵌套函数
        Universe.select_universe_difficulty(d)

        time.sleep(1)

        if auto.click_element("./assets/images/screen/universe/download_char.png", "image", 0.9,max_retries=10):
            time.sleep(1)
            Universe.clear_team(1)

            char_count=0
            auto.click_element_with_pos(((70, 300),(70, 300)), action="move")
            for character in config.universe_team[Utils.get_uid()]:
                time.sleep(0.5)
                if char_count == 4:
                    break
                logger.info(gu(f"{character}"))
                if not auto.click_element(f"./assets/images/character/{character}.png","image", 0.85, max_retries=10, take_screenshot=True):
                    time.sleep(0.5)
                    auto.mouse_scroll(30, -1)
                    if not auto.click_element(f"./assets/images/character/{character}.png", "image", 0.85, max_retries=10, take_screenshot=True):
                        time.sleep(0.5)
                        auto.mouse_scroll(30, 1)
                        continue
                    else:
                        logger.info(gu("该角色已选中"))
                        auto.mouse_scroll(30, 1)
                        char_count+=1
                else:
                    logger.info(gu("该角色已选中"))
                    char_count+=1
                time.sleep(0.5)
            if char_count == 4:
                return False
            else:
                logger.error(gu(f"{nowtime}模拟宇宙未能选中4位配置中的角色,请检查"))
                raise Exception(f"{nowtime}模拟宇宙未能选中4位配置中的角色,请检查")
        else:
            nowtime = time.time()
            logger.error(gu(f"{nowtime}模拟宇宙未找到下载角色按钮"))
            raise Exception(f"{nowtime}模拟宇宙未找到下载角色按钮")
              
    def select_universe_difficulty(d):
        difficulty_crop=(85.0 / 1920, 108.0 / 1080, 94.0 / 1920, 836.0 / 1080)
        if d==0:
            logger.error(gu(f"难度{d}不合法"))
            return

        if not auto.click_element(f"./assets/images/universe/on_{d}.png","image", 0.9, max_retries=5, crop=difficulty_crop):
                logger.info(gu(f"未选中难度{d}"))
                if not auto.click_element(f"./assets/images/universe/off_{d}.png","image", 0.9, max_retries=5, crop=difficulty_crop):
                    logger.info(gu(f"仍未选中难度{d}"))
                    auto.click_element_with_pos(((135, 160+(d-1)*110),(135, 160+(d-1)*110)))
                    if not auto.click_element(f"./assets/images/universe/on_{d}.png","image", 0.9, max_retries=5, crop=difficulty_crop):
                        Universe.select_universe_difficulty(d-1)
        
        logger.info(gu(f"已选中难度{d}"))
        return
    
    def clear_team(j):
        if j == 10:
            nowtime = time.time()
            logger.error(gu(f"{nowtime},模拟宇宙清理队伍失败"))
            raise Exception(f"{nowtime},模拟宇宙清理队伍失败")
        
        for i in range(4):
            auto.click_element_with_pos(((663+i*105, 837),(663+i*105, 837)))
            time.sleep(1)
        if auto.find_element("./assets/images/universe/all_clear_team.png", "image", 0.95, take_screenshot=True):
            logger.info(gu("队伍已清空"))
            return
        else:
            Universe.clear_team(j+1)

    @staticmethod
    def gui():
        if Universe.before_start():
            if subprocess.run(["start", "gui.exe"], shell=True, check=True, cwd=config.universe_path, env=config.env):
                return True
        return False
