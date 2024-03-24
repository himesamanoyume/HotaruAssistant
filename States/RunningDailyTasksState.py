from States import *
import time, datetime

class RunningDailyTasksState(BaseState):

    mStateName = 'RunningDailyTasksState'

    def OnBegin(self):
        log.hr(logMgr.Hr("今日实训"), 2)

        count = 0
        for key, value in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid].items():
            state = "\033[91m待完成\033[0m" if value else "\033[92m已完成\033[0m"
            log.info(logMgr.Info(f"{key}: {state}"))
            count = count + 1 if not value else count
        log.info(logMgr.Info(f"已完成:\033[93m{count}/{len(configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid])}\033[0m"))

        for taskName in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid].keys():
            if f"{taskName}" in dataMgr.dailyTasksFunctions.keys():
                if configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid][taskName]:
                    if configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid]:
                        log.info(logMgr.Info(f"因每日任务已完成,【{taskName}】\033[92m跳过\033[0m"))
                        continue
                    if dataMgr.dailyTasksFunctions[f"{taskName}"]():
                        log.info(logMgr.Info(f"{taskName}已完成"))
                        configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid][taskName] = False
                        # RunningDailyTasksState.ShowDailyTasksScore(taskName)
                        if taskName in dataMgr.meta['task_score_mappings'].keys():
                            log.info(logMgr.Info(f"{taskName}的活跃度为{dataMgr.meta['task_score_mappings'][taskName]}"))
                            self.CalcDailyTasksScore()                  
                    else:
                        if not configMgr.mConfig[configMgr.mKey.DAILY_TASKS_FIN][dataMgr.currentUid]:
                            log.warning(logMgr.Warning(f"【{taskName}】可能对应选项\033[91m未开启\033[0m,请自行解决"))
                else:
                    log.info(logMgr.Info(f"【{taskName}】该任务\033[92m已完成\033[0m,跳过"))
            else:
                log.warning(logMgr.Warning(f"【{taskName}】可能该任务\033[91m暂不支持\033[0m,跳过"))                                              
        
        count = 0
        for key, value in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid].items():
            count = count + 1 if not value else count

        log.info(logMgr.Info(f"已完成:\033[93m{count}/{len(configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataMgr.currentUid])}\033[0m"))
        self.CalcDailyTasksScore()

        log.hr(logMgr.Hr("完成日常任务部分结束"), 2)

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    # @staticmethod
    # def ShowDailyTasksScore(taskName):
    #     if taskName in dataMgr.meta['task_score_mappings'].keys():
    #         log.info(logMgr.Info(f"{taskName}的活跃度为{dataMgr.meta['task_score_mappings'][taskName]}"))
    #         BaseState.CalcDailyTasksScore()