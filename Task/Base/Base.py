from States.InitState import InitState
from States.StartGameState import StartGameState
from States.LoginGameState import LoginGameState
from Hotaru.Client.StateHotaru import stateMgr
from Hotaru.Client.DataClientHotaru import dataMgr
from States.DetectNewAccountState import DetectNewAccountState

class Base:
    @staticmethod
    def DetectNewAccount():
        stateMgr.Transition(DetectNewAccountState())

    @staticmethod
    def BeReadyToStart(uid):
        dataMgr.tempUid = uid
        stateMgr.Transition(InitState())
    
    @staticmethod
    def StartAndLoginGame():
        stateMgr.Transition(StartGameState())
        stateMgr.Transition(LoginGameState())