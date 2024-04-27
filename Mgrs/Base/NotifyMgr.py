from Modules.Utils.Notify import Notify

class NotifyMgr:
    def __init__(self):
        self.notify = Notify()

    def GetOfficialAnnList(self, isInformation = True):
        return self.notify.GetOfficialAnnList(isInformation)
    
    def GetGithubAnnList(self, dataMgr):
        return self.notify.GetGithubAnnList(dataMgr)
    
    def SendNotifyAll(self, title, content, configMgr, dataMgr):
        self.notify.SendNotifyAll(title, content, configMgr, dataMgr)

    def SendNotifySingle(self, title, subTitle, content, configMgr, dataMgr, uid):
        self.notify.SendNotifySingle(title, subTitle, content, configMgr, dataMgr, uid)

    def CreateUpdateContent(self, dataMgr):
        return self.notify.CreateHotaruUpdateContent(dataMgr)