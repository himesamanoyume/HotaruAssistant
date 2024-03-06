from States.InitState import InitState
from States.StartGameState import StartGameState
from States.LoginGameState import LoginGameState
from Hotaru.Client.StateHotaru import stateMgr
from Modules.Utils.ClientData import ClientData
from States.DetectNewAccountState import DetectNewAccountState

class Base:
    @staticmethod
    def DetectNewAccount():
        stateMgr.Transition(DetectNewAccountState())

    @staticmethod
    def ReadyToStart(uid):
        ClientData.tempUid = uid
        stateMgr.Transition(InitState())
    
    @staticmethod
    def SetupGame():
        stateMgr.Transition(StartGameState())
        stateMgr.Transition(LoginGameState())
        stateMgr.Transition(StartGameState())