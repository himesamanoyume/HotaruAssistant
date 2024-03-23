
from Hotaru.Client.LogClientHotaru import logMgr,log
from States.InitState import InitState
from States.StartGameState import StartGameState
from States.InitAccountState import InitAccountState
from Hotaru.Client.StateHotaru import stateMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from States.DetectNewAccountState import DetectNewAccountState
from States.QuitGameState import QuitGameState
from States.WaitForNextLoopState import WaitForNextLoopState
from States.GetPowerInfoState import GetPowerInfoState
from States.InitDailyTasksState import InitDailyTasksState
from States.RunningDailyTasksState import RunningDailyTasksState
from States.DailyEchoOfWarState import DailyEchoOfWarState
from States.DailyClearPowerState import DailyClearPowerState
from States.GetUniverseInfoState import GetUniverseInfoState
from States.GetRelicsInfoState import GetRelicsInfoState
from States.GetFAndPInfoState import GetFAndPInfoState
from States.DailyGetRewardState import DailyGetRewardState

class TaskMgr:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance
    
    @staticmethod
    def StartGame():
        dataMgr.currentAction = "登录流程"
        if stateMgr.Transition(StartGameState()):
            stateMgr.Transition(InitAccountState())
            return True # 为True时才会进行每日任务流程或模拟宇宙流程
            
    @staticmethod
    def QuitGame(uid:str, lastUid:str):
        stateMgr.Transition(QuitGameState())

    @staticmethod
    def DetectNewAccounts():
        stateMgr.Transition(DetectNewAccountState())

    @staticmethod
    def ReadyToStart(uid):
        dataMgr.tempUid = uid
        stateMgr.Transition(InitState())

    @staticmethod
    def WaitForNextLoop():
        stateMgr.Transition(WaitForNextLoopState())

    @staticmethod
    def StartDaily():
        log.hr(logMgr.Hr(f"进入{dataMgr.currentAction}"))
        # InitDailyTasksState返回True时将跳过每日任务流程
        if not stateMgr.Transition(InitDailyTasksState()):
            # 做每日
            stateMgr.Transition(RunningDailyTasksState())
            stateMgr.Transition(GetPowerInfoState())
            if not stateMgr.Transition(DailyEchoOfWarState()):
                # 如果有历战余响可打,打完后需要再获取一次体力
                stateMgr.Transition(GetPowerInfoState())
            # 清体力
            stateMgr.Transition(DailyClearPowerState())
            stateMgr.Transition(DailyGetRewardState())
            # 获取体力信息
            stateMgr.Transition(GetPowerInfoState())
            # 获取模拟宇宙积分信息
            stateMgr.Transition(GetUniverseInfoState())
            # 获取遗器,副本倒计时信息
            stateMgr.Transition(GetRelicsInfoState())
            stateMgr.Transition(GetFAndPInfoState())
        else:
            pass

    @staticmethod
    def StartUniverse():
        log.hr(logMgr.Hr(f"进入{dataMgr.currentAction}"))
        return