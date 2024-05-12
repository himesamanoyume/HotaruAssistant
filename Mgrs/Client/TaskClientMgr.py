
from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.StateClientHotaru import stateClientMgr
from Hotaru.Client.DataClientHotaru import dataClientMgr
from States.Client.ClientStartGameState import ClientStartGameState
from States.Client.ClientInitAccountState import ClientInitAccountState
from States.Client.ToolsInitAccountState import ToolsInitAccountState
from States.Client.QuitGameState import QuitGameState
from States.Client.SendEmailState import SendEmailState
from States.Client.SendEmailExceptionState import SendEmailExceptionState
from States.Client.DetectNewAccountState import DetectNewAccountState
from States.Client.InitState import InitState
from States.Client.WaitForNextLoopState import WaitForNextLoopState
from States.Client.GetPowerInfoState import GetPowerInfoState
from States.Client.InitDailyTasksState import InitDailyTasksState
from States.Client.RunningDailyTasksState import RunningDailyTasksState
from States.Client.DailyEchoOfWarState import DailyEchoOfWarState
from States.Client.DailyClearPowerState import DailyClearPowerState
from States.Client.GetUniverseRewardAndInfoState import GetUniverseRewardAndInfoState
from States.Client.GetRelicsInfoState import GetRelicsInfoState
from States.Client.GetFAndPInfoState import GetFAndPInfoState
from States.Client.GetRewardState import GetRewardState
from States.Client.UniverseClearState import UniverseClearState
from States.Client.CheckCdkeyState import CheckCdkeyState
from States.Client.CheckStoreState import CheckStoreState
import time
from Mgrs.Base.TaskBaseMgr import TaskBaseMgr

class TaskClientMgr(TaskBaseMgr):
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls, logMgr,log, stateClientMgr, dataClientMgr)

        return cls.mInstance
    
    def ClientStartGame(self):
        dataClientMgr.currentAction = "登录流程"
        dataClientMgr.loopStartTimestamp = time.time()
        if stateClientMgr.Transition(ClientStartGameState()):
            stateClientMgr.Transition(ClientInitAccountState())
            return True # 为True时才会进行每日任务流程或模拟宇宙流程
        
    def ToolsStartGame(self):
        dataClientMgr.currentAction = "登录流程"
        if stateClientMgr.Transition(ClientStartGameState()):
            stateClientMgr.Transition(ToolsInitAccountState())
            return True # 为True时才会进行每日任务流程或模拟宇宙流程
            
    def QuitGame(self):
        stateClientMgr.Transition(QuitGameState())

    def SendNotify(self):
        stateClientMgr.Transition(SendEmailState())

    def SendExceptionNotify(self, e):
        dataClientMgr.tempText = e
        stateClientMgr.Transition(SendEmailExceptionState())

    def DetectNewAccounts(self):
        stateClientMgr.Transition(DetectNewAccountState())

    def ReadyToStart(self, uid):
        dataClientMgr.tempUid = uid
        stateClientMgr.Transition(InitState())

    def WaitForNextLoop(self):
        stateClientMgr.Transition(WaitForNextLoopState())
    
    @staticmethod
    def StartDaily():
        log.hr(logMgr.Hr(f"进入{dataClientMgr.currentAction}"))
        # InitDailyTasksState返回True时将跳过每日任务流程
        if not stateClientMgr.Transition(InitDailyTasksState()):
            stateClientMgr.Transition(GetPowerInfoState())
            # 获取模拟宇宙积分/沉浸器信息
            stateClientMgr.Transition(GetUniverseRewardAndInfoState())
            if not stateClientMgr.Transition(DailyEchoOfWarState()):
                # 如果有历战余响可打,打完后需要再获取一次体力信息
                stateClientMgr.Transition(GetPowerInfoState())
                # 再获取一次历战余响信息
                stateClientMgr.Transition(DailyEchoOfWarState())
            # 清体力
            if not stateClientMgr.Transition(DailyClearPowerState()):
                # 如果有清体力可打,打完后需要再获取一次体力信息
                stateClientMgr.Transition(GetPowerInfoState())
                # 领奖励
                stateClientMgr.Transition(GetRewardState())
            # 做每日
            stateClientMgr.Transition(RunningDailyTasksState())
            # 领奖励
            stateClientMgr.Transition(GetRewardState())
            # 检查兑换码
            stateClientMgr.Transition(CheckCdkeyState())
            # 获取遗器,副本倒计时,月卡倒计时信息
            stateClientMgr.Transition(GetRelicsInfoState())
            stateClientMgr.Transition(GetFAndPInfoState())
            stateClientMgr.Transition(CheckStoreState())
        else:
            pass

    @staticmethod
    def StartUniverse():
        log.hr(logMgr.Hr(f"进入{dataClientMgr.currentAction}"))
        # 获取遗器,副本倒计时信息
        if not stateClientMgr.Transition(GetRelicsInfoState()):
            # 如果遗器数量未超标,则进行获取模拟宇宙积分/沉浸器信息,开始模拟宇宙
            # 获取体力信息
            stateClientMgr.Transition(GetPowerInfoState())
            stateClientMgr.Transition(GetUniverseRewardAndInfoState())
            stateClientMgr.Transition(UniverseClearState())
        # 领奖励
        stateClientMgr.Transition(GetRewardState())
        # 获取体力信息
        stateClientMgr.Transition(GetPowerInfoState())
        # 获取模拟宇宙积分信息
        stateClientMgr.Transition(GetUniverseRewardAndInfoState())
        # 获取遗器,副本倒计时信息,月卡倒计时信息
        stateClientMgr.Transition(GetRelicsInfoState())
        stateClientMgr.Transition(GetFAndPInfoState())
        stateClientMgr.Transition(CheckStoreState())