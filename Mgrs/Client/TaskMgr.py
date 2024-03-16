
from Hotaru.Client.LogClientHotaru import logMgr,log
from States.InitState import InitState
from States.StartGameState import StartGameState
from States.LoginGameState import LoginGameState
from Hotaru.Client.StateHotaru import stateMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from States.DetectNewAccountState import DetectNewAccountState
from States.QuitGameState import QuitGameState
from States.WaitForNextLoopState import WaitForNextLoopState

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
            stateMgr.Transition(LoginGameState())
            return True
            
    @staticmethod
    def QuitGame():
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
    def StartDaily(expectUid, lastUid):
        log.info(logMgr.Info(f"{dataMgr.currentAction}:进入每日"))
        return

    @staticmethod
    def StartUniverse(expectUid, lastUid):
        log.info(logMgr.Info(f"{dataMgr.currentAction}:进入模拟宇宙"))
        return