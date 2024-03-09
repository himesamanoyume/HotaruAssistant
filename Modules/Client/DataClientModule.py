
class DataClient:
    tempUid = -1
    currentUid = -1
    currentGamePid = -1 # 初始值 不要动
    loginDict = dict()
    loginList = list()
    loopStartTimestamp = 0
    currentAction = "临时流程"

    def ResetData(self):
        self.currentUid = -1
        self.currentGamePid = -1
        self.loopStartTimestamp = 0
        self.currentAction = "临时流程"
