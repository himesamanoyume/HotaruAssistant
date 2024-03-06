from Hotaru.Client.LogClientHotaru import logClientMgr,log
from Modules.Client.OcrModule import OcrModule
import os,cpufeature,sys

if cpufeature.CPUFeature["AVX2"]:
    ocrName = "PaddleOCR-json"
    ocrPath = r".\3rdparty\PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe"
    log.debug(logClientMgr.Debug("CPU 支持 AVX2 指令集，使用 PaddleOCR-json"))
else:
    ocrName = "RapidOCR-json"
    ocrPath = r".\3rdparty\RapidOCR-json_v0.2.0\RapidOCR-json.exe"
    log.debug(logClientMgr.Debug("CPU 不支持 AVX2 指令集，使用 RapidOCR-json"))

class OcrClientMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mOcr = OcrModule(ocrPath)

        return cls.mInstance
    
    @classmethod
    def CheckPath(cls):
        if not os.path.exists(ocrPath):
            log.warning(logClientMgr.Warning(f"OCR 路径不存在: {ocrPath}, 请重新启动Server对OCR进行检测下载..."))
            input("按回车关闭窗口...")
            sys.exit(0)

