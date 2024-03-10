from Modules.Server.NotifyModule import NotifyModule

class NotifyMgr:
    def __init__(self):
        self.notify = NotifyModule()

    def CreateOfficialNotice(self):
        return self.notify.CreateOfficialNotice()