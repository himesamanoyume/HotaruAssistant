from Hotaru.Server.LogServerHotaru import logMgr
import os,cpufeature

if cpufeature.CPUFeature["AVX2"]:
    ocrName = "PaddleOCR-json"
    ocrPath = r".\3rdparty\PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe"
else:
    ocrName = "RapidOCR-json"
    ocrPath = r".\3rdparty\RapidOCR-json_v0.2.0\RapidOCR-json.exe"

class OcrServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)

        return cls.mInstance

    @staticmethod
    def InstallOCR():
        from Hotaru.Server.UpdateHotaru import updateMgr
        from Modules.Utils.FastestMirror import FastestMirror
        if ocrName == "PaddleOCR-json":
            url = FastestMirror.GetGithubMirror("https://github.com/hiroi-sora/PaddleOCR-json/releases/download/v1.3.1/PaddleOCR-json_v.1.3.1.7z")
            updateMgr.mUpdate.InitUpdateHandler(url, os.path.dirname(ocrPath), "PaddleOCR-json_v.1.3.1")
        elif ocrName == "RapidOCR-json":
            url = FastestMirror.GetGithubMirror("https://github.com/hiroi-sora/RapidOCR-json/releases/download/v0.2.0/RapidOCR-json_v0.2.0.7z")
            updateMgr.mUpdate.InitUpdateHandler(url, os.path.dirname(ocrPath), "RapidOCR-json_v0.2.0")

        updateMgr.mUpdate.Run()

    @classmethod
    def CheckPath(cls):
        if not os.path.exists(ocrPath):
            logMgr.Warning(f"OCR 路径不存在: {ocrPath}, 即将开始下载")
            cls.InstallOCR()
