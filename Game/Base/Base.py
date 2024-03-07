from States.InitState import InitState
from States.StartGameState import StartGameState
from States.LoginGameState import LoginGameState
from Hotaru.Client.StateHotaru import stateMgr
from Hotaru.Client.DataHotaru import data
from States.DetectNewAccountState import DetectNewAccountState

class Base:
    @staticmethod
    def DetectNewAccount():
        stateMgr.Transition(DetectNewAccountState())

    @staticmethod
    def ReadyToStart(uid):
        data.tempUid = uid
        stateMgr.Transition(InitState())
    
    @staticmethod
    def SetupGame():
        stateMgr.Transition(StartGameState())
        stateMgr.Transition(LoginGameState())