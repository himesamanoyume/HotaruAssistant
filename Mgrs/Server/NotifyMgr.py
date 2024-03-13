from Modules.Utils.Notify import Notify

class NotifyMgr:
    def __init__(self):
        self.notify = Notify()

    def CreateOfficialNotice(self):
        return self.notify.CreateOfficialNotice()
    
    def CreateAnnList(self, dataMgr):
        return self.notify.CreateAnnList(dataMgr)
    
    def SendNotifyAll(self, title, content, configMgr, dataMgr):
        self.notify.SendNotifyAll(title, content, configMgr, dataMgr)

    def SendNotifySingle(self, title, content, configMgr, dataMgr, uid, singleTo=''):
        self.notify.SendNotifySingle(title, content, configMgr, dataMgr, uid, singleTo)

    def CreateUpdateContent(self, dataMgr):
        return self.notify.CreateUpdateContent(dataMgr)