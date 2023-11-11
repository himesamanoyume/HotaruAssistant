from managers.config_manager import config
from managers.logger_manager import logger
from managers.automation_manager import auto
from datetime import datetime
import time
from managers.ocr_manager import ocr
from tasks.base.date import Date
from managers.translate_manager import _
import json
import sys

class Utils:
    _uid = '-1'
    _daily_tasks = {}
    _task_mappings = {}
    _task_score_mappings = {}
    _content = dict()
    _power = 250
    _temp = ''
    _start_timestamp = 0
    _loop_start_timestamp = 0
    def detectIsNoneButNoSave(configName, uid, defaultValue=0):
        if configName == {} or uid not in configName.keys():
            configName[uid] = defaultValue
        elif configName[uid] == None:
            configName[uid] = defaultValue

    def saveTimestamp(timestamp, uid):
        if config.save_timestamp(timestamp, uid):
            logger.info(_("已更新时间戳"))
        else:
            logger.info(_("更新时间戳出错"))

    def getFullPowerTime(power):
        remainingPower = 240 - power
        timestamp = remainingPower * 360 + time.time()
        _datetime = datetime.fromtimestamp(timestamp)
        return _datetime
    
    def get_universe_score():
        score_crop = (267.0 / 1920, 738.0 / 1080, 271.0 / 1920, 57.0 / 1080)
        time.sleep(1)
        try:
            scoreAndMaxScore = auto.get_single_line_text(crop=score_crop, blacklist=[], max_retries=5)
            logger.info(_(f"识别到文字为:{scoreAndMaxScore}"))
            Utils.detectIsNoneButNoSave(config.universe_score, Utils.get_uid())
            config.universe_score[Utils.get_uid()] = scoreAndMaxScore
            config.save_config()

            current_score = scoreAndMaxScore.split('/')[0]
            max_score = scoreAndMaxScore.split('/')[1]

            logger.info(_(f"识别到当前积分为:{current_score}"))
            logger.info(_(f"识别到积分上限为:{max_score}"))
            if int(current_score) == int(max_score):
                logger.info(_(f"模拟宇宙积分已满"))
                config.universe_fin[Utils.get_uid()] = True
            else:
                logger.info(_(f"模拟宇宙积分未满"))
                config.universe_fin[Utils.get_uid()] = False
                
            config.save_config()
            return int(current_score), int(max_score)
        except Exception as e:
            logger.error(_("识别模拟宇宙积分失败: {error}").format(error=e))
            config.universe_score[Utils.get_uid()] = '0/1'
            config.save_config()
            logger.warning(_("因读取模拟宇宙积分失败,程序中止"))

    def init_instanceButNoSave(uid):
        if config.instance_type == {} or uid not in config.instance_type.keys():
            config.instance_type[uid] = '拟造花萼（金）'

        if config.instance_names == {} or uid not in config.instance_names.keys():
            config.instance_names[uid] = {}
            config.instance_names[uid]['拟造花萼（金）'] = '回忆之蕾'
            config.instance_names[uid]['拟造花萼（赤）'] = '毁灭之蕾'
            config.instance_names[uid]['凝滞虚影'] = '无'
            config.instance_names[uid]['侵蚀隧洞'] = '睿治之径'
            config.instance_names[uid]['历战余响'] = '毁灭的开端'

    def get_new_uid():
        uid_crop = (70.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080)
        try:
            Utils._uid = auto.get_single_line_text(crop=uid_crop, blacklist=[], max_retries=9)
            Utils._content = dict()
            Utils._temp = ''
            Utils._power = 250
            Utils._content['relic_content'] = ''
            Utils._content['universe_number'] = ''
            Utils._content['universe_difficulty'] = ''
            Utils._content['universe_fate'] = ''
            Utils._start_timestamp = time.time()
            logger.info(_(f"识别到UID为:{Utils._uid}"))
            config.set_value('last_running_uid', Utils._uid)
        except Exception as e:
            nowtime = time.time()
            logger.error(f"{nowtime},识别UID失败: {e}")
            raise Exception(f"{nowtime},识别UID失败: {e}")
        
    def get_uid():
        if Utils._uid == '-1':
            Utils.get_new_uid()
            return Utils._uid
        else:
            return Utils._uid
        
    def showDailyTasksScore(task_name, uid):
        Utils.detectIsNoneButNoSave(config.daily_tasks_score, uid)
        config.save_config()
        if task_name in Utils._task_score_mappings.keys():
            logger.info(_(f"{task_name}的活跃度为{Utils._task_score_mappings[task_name]}"))
            Utils.calcDailyTasksScore(uid)

    def calcDailyTasksScore(uid):
        config.daily_tasks_score[uid] = 0
        temp_score = 0
        i=0
        for key, value in config.daily_tasks[uid].items():
            Utils._content.update({f'daily_0{i}_score':f'{Utils._task_score_mappings[key]}'})
            i+=1
            if not value:
                temp_score += Utils._task_score_mappings[key]
        
        config.daily_tasks_score[uid] = temp_score
        config.save_config()
        logger.info(_(f"现在总活跃度为{config.daily_tasks_score[uid]}"))

        if config.daily_tasks_score[uid] >= 500:
            config.daily_tasks_fin[uid] = True
            logger.info(_("该账号今日500活跃度已达成"))
        elif config.daily_tasks_fin[uid]:
            config.daily_tasks_fin[uid] = False
            logger.info(_("该账号今日500活跃度未达成"))

        config.save_config()
    
    def getDailyScoreMappings():
        Utils._task_score_mappings = Utils._load_config("./assets/config/task_score_mappings.json")
        
    def getConfigValue(configKey, uid):
        Utils.detectIsNoneButNoSave(configKey, uid)
        config.save_config()
        return configKey[uid]
        
    def is_next_4_am(timestamp, uid, isLog=True):
        Utils.detectIsNoneButNoSave(timestamp, uid)
        return Date.is_next_4_am(timestamp[uid], isLog)
    
    def is_next_mon_4_am(timestamp, uid, isLog=True):
        Utils.detectIsNoneButNoSave(timestamp, uid)
        return Date.is_next_mon_4_am(timestamp[uid], isLog)
    
    def click_element_quest(target, find_type, threshold=None, max_retries=1, crop=(0, 0, 0, 0), take_screenshot=True, relative=False, scale_range=None, include=None, need_ocr=True, source=None, offset=(0, 0)):
        coordinates = auto.find_element(target, find_type, threshold, max_retries, crop, take_screenshot,
                                        relative, scale_range, include, need_ocr, source)
        if coordinates:
            logger.warning("检测到每日任务待领取")
            return Utils.click_element_with_pos_quest(coordinates, offset)
        return False
    
    def _load_config(config_example_path):
        try:
            with open(config_example_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(_("配置文件不存在：{path}").format(path=config_example_path))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)
    
    def click_element_with_pos_quest(coordinates, offset=(0, 0), action="click"):
        auto.take_screenshot(crop=(297.0 / 1920, 478.0 / 1080, 246.0 / 1920, 186.0 / 1080))
        time.sleep(2)
        result = ocr.recognize_multi_lines(auto.screenshot)
        result_keyword = result[0][1][0]
        time.sleep(0.5)
        Utils._task_mappings = Utils._load_config("./assets/config/task_mappings.json")
        for mappings_keyword, task_name in Utils._task_mappings.items():
            logger.info(f"keyword:{mappings_keyword}")
            if mappings_keyword == result_keyword:
                if task_name in config.daily_tasks[Utils.get_uid()] and config.daily_tasks[Utils.get_uid()][task_name] == True:
                    config.daily_tasks[Utils.get_uid()][task_name] = False
                    logger.warning(_(f"keyword:{mappings_keyword}----->{task_name}:进行了点击,任务已经完成"))
                    Utils.showDailyTasksScore(task_name, Utils.get_uid())
                    config.save_config()
                else:
                    logger.warning(_(f"keyword:{mappings_keyword}----->{task_name}:进行了点击,但可能配置项中之前已完成修改或未识别成功"))
                break
        (left, top), (right, bottom) = coordinates
        x = (left + right) // 2 + offset[0]
        y = (top + bottom) // 2 + offset[1]
        if action == "click":
            auto.mouse_click(x, y)
        elif action == "down":
            auto.mouse_down(x, y)
        elif action == "move":
            auto.mouse_move(x, y)
        return True