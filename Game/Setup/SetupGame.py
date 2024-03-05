from States.InitState import InitState
from States.StartGameState import StartGameState
from States.LoginGameState import LoginGameState
from Hotaru.Client.StateHotaru import stateMgr

class SetupGame:
    
    @staticmethod
    def SetupGame():
        stateMgr.Transition(InitState())
        stateMgr.Transition(StartGameState())
        stateMgr.Transition(LoginGameState())
        stateMgr.Transition(StartGameState())