from Modules.Common.OcrBaseModule import OcrBaseModule
import os,sys

class OcrBaseMgr:
    mInstance = None
    
    def __new__(cls, ocrPath, logMgr, log):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.logMgr = logMgr
            cls.log = log
            cls.mOcr = OcrBaseModule(ocrPath, logMgr, log)

        return cls.mInstance
    
    @classmethod
    def CheckPath(cls):
        if not os.path.exists(cls.mOcr.ocrPath):
            cls.log.warning(cls.logMgr.Warning(f"OCR 路径不存在: {cls.mOcr.ocrPath}, 请重新启动Server对OCR进行检测下载..."))
            input("按回车关闭窗口...")
            sys.exit(0)

