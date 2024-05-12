from Modules.Utils.Date import Date
import os,shutil

class InitUidConfig:
    @staticmethod
    def InitUidDefaultConfig(configMgr, log, logMgr, uid):
        try:
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.RELICS_SALVAGE_ENABLE, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.RELICS_SALVAGE_4STAR_ENABLE, uid, True)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.RELICS_SALVAGE_5STAR_ENABLE, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.RELICS_SALVAGE_5STAR_TO_EXP, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.RELICS_THRESHOLD_COUNT, uid, 1450)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.ECHO_OF_WAR_ENABLE, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.ECHO_OF_WAR_TIMES, uid, 3)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.ECHO_OF_WAR_TIMESTAMP, uid)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FIN, uid, False)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_NUMBER, uid, 3)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_DIFFICULTY, uid, 1)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FATE, uid, 4)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_TEAM, uid, {})
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_SCORE, uid, '0/1')
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_BONUS_ENABLE, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_SPEED_ENABLE, uid, False)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.BORROW_CHARACTER_ENABLE, uid, False)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.INSTANCE_TEAM_ENABLE, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.USE_RESERVED_TRAILBLAZE_POWER, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.USE_FUEL, uid, False)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.FORGOTTENHALL_STARS, uid, 0)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.FORGOTTENHALL_LEVELS, uid, 0)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.PUREFICTION_STARS, uid, 0)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.PUREFICTION_LEVELS, uid, 0)

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.LAST_RUN_TIMESTAMP, uid)

            if configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE] == {} or uid not in configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE].keys():
                configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid] = {}
                tempList = list()
                tempList.append('拟造花萼（金）')
                configMgr.mConfig[configMgr.mKey.INSTANCE_TYPE][uid] = tempList

            if configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER] == {} or uid not in configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER].keys() or not isinstance(configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid], dict):
                configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid] = {}
                configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid]['默认配队'] = 0
                configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid]['拟造花萼（金）'] = 0
                configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid]['拟造花萼（赤）'] = 0
                configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid]['凝滞虚影'] = 0
                configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid]['侵蚀隧洞'] = 0
                configMgr.mConfig[configMgr.mKey.INSTANCE_TEAM_NUMBER][uid]['历战余响'] = 0
            
            if configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES] == {} or uid not in configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES].keys():
                configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid] = {}
                configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['拟造花萼（金）'] = '雅利洛-回忆之蕾'
                configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['拟造花萼（赤）'] = '毁灭之蕾1'
                configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['凝滞虚影'] = '空海之形'
                configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['侵蚀隧洞'] = '睿治之径'
                configMgr.mConfig[configMgr.mKey.INSTANCE_NAMES][uid]['历战余响'] = '毁灭的开端'

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS_SCORE, uid, 0)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS_FIN, uid, False)
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.DAILY_TASKS, uid, {})

            if Date.IsNext4AM(configMgr.mConfig[configMgr.mKey.LAST_RUN_TIMESTAMP][uid], False):
                configMgr.mConfig[configMgr.mKey.DAILY_TASKS_SCORE][uid] = 0
                configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][uid] = False
                configMgr.mConfig[configMgr.mKey.DAILY_TASKS][uid] = {}
                if os.path.exists(f"./screenshots/{uid}"):
                    shutil.rmtree(f"./screenshots/{uid}")
                

            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_TIMESTAMP, uid)
            maxScore = str(configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][uid]).split('/')[1]
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_SCORE, uid, f"0/{maxScore}")
            configMgr.mConfig.DetectKeyIsExist(configMgr.mKey.UNIVERSE_FIN, uid, False)

            if Date.IsNextMon4AM(configMgr.mConfig[configMgr.mKey.UNIVERSE_TIMESTAMP][uid], False):
                configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][uid] = f"0/{maxScore}"
                configMgr.mConfig[configMgr.mKey.UNIVERSE_FIN][uid] = False

            return True

        except Exception as e:
            log.error(logMgr.Error(f"发生错误:{e}"))
            return False
