from Hotaru.Client.LogClientHotaru import logMgr,log
from Mgrs.Base.OcrBaseMgr import OcrBaseMgr
import cpufeature

class OcrClientMgr(OcrBaseMgr):
    def __new__(cls):
        if cls.mInstance is None:
            if cpufeature.CPUFeature["AVX2"]:
                ocrName = "PaddleOCR-json"
                ocrPath = r".\3rdparty\PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe"
                log.debug(logMgr.Debug("CPU 支持 AVX2 指令集，使用 PaddleOCR-json"))
            else:
                ocrName = "RapidOCR-json"
                ocrPath = r".\3rdparty\RapidOCR-json_v0.2.0\RapidOCR-json.exe"
                log.debug(logMgr.Debug("CPU 不支持 AVX2 指令集，使用 RapidOCR-json"))

            cls.mInstance = super().__new__(cls, ocrPath, logMgr, log)

        return cls.mInstance
