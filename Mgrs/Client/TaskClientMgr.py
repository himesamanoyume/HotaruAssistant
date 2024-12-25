
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
from States.Client.DivergentUniverseClearState import DivergentUniverseClearState
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
            return True # 为True时才会进行每日任务流程或差分宇宙流程
        
    def ToolsStartGame(self):
        dataClientMgr.currentAction = "登录流程"
        if stateClientMgr.Transition(ClientStartGameState()):
            stateClientMgr.Transition(ToolsInitAccountState())
            return True # 为True时才会进行每日任务流程或差分宇宙流程
            
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

    def WaitForNextLoop(self, customWaitTime = 0):
        stateClientMgr.Transition(WaitForNextLoopState(customWaitTime))

    @staticmethod
    def StartDaily():
        # InitDailyTasksState返回True时将跳过每日任务流程
        if not stateClientMgr.Transition(InitDailyTasksState()): 
            stateClientMgr.Transition(GetPowerInfoState()) 
            if not stateClientMgr.Transition(DailyEchoOfWarState()): 
                # 如果有历战余响可打,打完后需要再获取一次体力信息
                stateClientMgr.Transition(GetPowerInfoState()) 
                # 再获取一次历战余响信息
                stateClientMgr.Transition(DailyEchoOfWarState()) 
            # 获取差分宇宙积分/沉浸器信息
            stateClientMgr.Transition(GetUniverseRewardAndInfoState()) 
            # 直接进行差分宇宙
            if not stateClientMgr.Transition(DivergentUniverseClearState()): 
                # 再次获取差分宇宙积分/沉浸器信息
                stateClientMgr.Transition(GetUniverseRewardAndInfoState()) 
            # 清体力,检测遗器数量
            hasBeenDetectedRelicsCountAndPowerHasBeenCleanedUp = False
            if not stateClientMgr.Transition(DailyClearPowerState()): 
                # 如果有清体力可打,打完后需要再获取一次体力信息
                stateClientMgr.Transition(GetPowerInfoState()) 
                # 领奖励
                stateClientMgr.Transition(GetRewardState()) 
                hasBeenDetectedRelicsCountAndPowerHasBeenCleanedUp = True
            # 做每日
            stateClientMgr.Transition(RunningDailyTasksState()) 
            # 领奖励
            stateClientMgr.Transition(GetRewardState()) 
            # 检查兑换码
            stateClientMgr.Transition(CheckCdkeyState()) 
            # 获取遗器,副本倒计时,月卡倒计时信息
            if hasBeenDetectedRelicsCountAndPowerHasBeenCleanedUp:
                stateClientMgr.Transition(GetRelicsInfoState()) 
            stateClientMgr.Transition(GetFAndPInfoState()) 
            stateClientMgr.Transition(CheckStoreState()) 