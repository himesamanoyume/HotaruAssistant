
class DataClient:
    tempUid = -1
    currentUid = -1
    loginDict = dict()
    loginList = list()
    loopStartTimestamp = 0

    def ResetData(self):
        self.currentUid = -1
        self.loopStartTimestamp = 0
