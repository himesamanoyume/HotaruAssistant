
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
from States.GetUniverseRewardAndInfoState import GetUniverseRewardAndInfoState
from States.GetRelicsInfoState import GetRelicsInfoState
from States.GetFAndPInfoState import GetFAndPInfoState
from States.GetRewardState import GetRewardState
from States.SendEmailState import SendEmailState
from States.SendEmailExceptionState import SendEmailExceptionState
from States.UniverseClearState import UniverseClearState
from States.CheckCdkeyState import CheckCdkeyState
from States.CheckStoreState import CheckStoreState

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
    def QuitGame():
        stateMgr.Transition(QuitGameState())

    @staticmethod
    def SendNotify():
        stateMgr.Transition(SendEmailState())

    @staticmethod
    def SendExceptionNotify(e):
        dataMgr.tempText = e
        stateMgr.Transition(SendEmailExceptionState())

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
                # 如果有历战余响可打,打完后需要再获取一次体力信息
                stateMgr.Transition(GetPowerInfoState())
            # 清体力
            if not stateMgr.Transition(DailyClearPowerState()):
                # 如果有清体力可打,打完后需要再获取一次体力信息
                stateMgr.Transition(GetPowerInfoState())
            # 领奖励
            stateMgr.Transition(GetRewardState())
            # 检查兑换码
            stateMgr.Transition(CheckCdkeyState())
            # 获取模拟宇宙积分/沉浸器信息
            stateMgr.Transition(GetUniverseRewardAndInfoState())
            # 获取遗器,副本倒计时,月卡倒计时信息
            stateMgr.Transition(GetRelicsInfoState())
            stateMgr.Transition(GetFAndPInfoState())
            stateMgr.Transition(CheckStoreState())
        else:
            pass

    @staticmethod
    def StartUniverse():
        log.hr(logMgr.Hr(f"进入{dataMgr.currentAction}"))
        # 获取遗器,副本倒计时信息
        if not stateMgr.Transition(GetRelicsInfoState()):
            # 如果遗器数量未超标,则进行获取模拟宇宙积分/沉浸器信息,开始模拟宇宙
            stateMgr.Transition(GetUniverseRewardAndInfoState())
            stateMgr.Transition(UniverseClearState())
        # 领奖励
        stateMgr.Transition(GetRewardState())
        # 获取体力信息
        stateMgr.Transition(GetPowerInfoState())
        # 获取模拟宇宙积分信息
        stateMgr.Transition(GetUniverseRewardAndInfoState())
        # 获取遗器,副本倒计时信息,月卡倒计时信息
        stateMgr.Transition(GetRelicsInfoState())
        stateMgr.Transition(GetFAndPInfoState())
        stateMgr.Transition(CheckStoreState())