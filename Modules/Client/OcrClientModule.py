from Hotaru.Client.LogClientHotaru import logMgr,log
from Modules.Common.OcrBaseModule import OcrBaseModule

class OcrClientModule(OcrBaseModule):
    def __init__(self, exePath):
        super().__init__(exePath, logMgr, log)

