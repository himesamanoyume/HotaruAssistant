
from Hotaru.Client.LogClientHotaru import logMgr,log
from States.InitState import InitState
from States.StartGameState import StartGameState
from States.InitAccountState import InitAccountState
from Hotaru.Client.StateHotaru import stateMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from States.DetectNewAccountState import DetectNewAccountState
from States.QuitGameState import QuitGameState
from States.WaitForNextLoopState import WaitForNextLoopState
from States.GetPowerState import GetPowerState
from States.InitDailyTasksState import InitDailyTasksState
from States.RunningDailyTasksState import RunningDailyTasksState

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
            stateMgr.Transition(GetPowerState())
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
            stateMgr.Transition(RunningDailyTasksState())
        else:
            pass

    @staticmethod
    def StartUniverse():
        log.hr(logMgr.Hr(f"进入{dataMgr.currentAction}"))
        return