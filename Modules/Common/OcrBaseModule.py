from .PPOcrApiSubModule import GetOcrApi
from PIL import Image
import os,io

class OcrBaseModule:
    def __init__(self, ocrPath, logMgr, log):
        self.ocrPath = ocrPath
        self.logMgr = logMgr
        self.log = log
        self.ocr = None

    def InstanceOcr(self):
        if self.ocr is None:
            try:
                self.log.debug(self.logMgr.Debug("开始初始化OCR..."))
                self.ocr = GetOcrApi(self.ocrPath)
                self.log.debug(self.logMgr.Debug("初始化OCR完成"))
            except Exception as e:
                self.log.error(self.logMgr.Error(f"初始化OCR失败：{e}"))
                self.ocr = None
                self.log.info(self.logMgr.Info("请尝试重新下载或解压"))
                self.log.info(self.logMgr.Info("若 Win7 报错计算机中丢失 VCOMP140.DLL，请安装 VC运行库"))
                self.log.info(self.logMgr.Info("https://aka.ms/vs/17/release/vc_redist.x64.exe"))
                raise Exception (f"初始化OCR失败：{e}")
                # input("按回车键关闭窗口. . ."))
                # sys.exit(1)

    def ExitOcr(self):
        if self.ocr is not None:
            self.ocr.exit()
            self.ocr = None

    def ConvertFormat(self, result):
        if result['code'] != 100:
            self.log.debug(self.logMgr.Debug(result))
            return False
        convertedResult = []

        for item in result['data']:
            box = item['box']
            text = item['text']
            score = item['score']

            convertedItem = [
                [box[0], box[1], box[2], box[3]],
                (text, score)
            ]

            convertedResult.append(convertedItem)

        return convertedResult

    def Run(self, image):
        self.InstanceOcr()
        try:
            if isinstance(image, Image.Image):
                pass
            elif isinstance(image, str):
                return self.ocr.run(os.path.abspath(image))
            else:  # 默认为 np.ndarray，避免需要import numpy
                image = Image.fromarray(image)
            image_stream = io.BytesIO()
            image.save(image_stream, format="PNG")
            imageBytes = image_stream.getvalue()
            originalDict = self.ocr.runBytes(imageBytes)

            replacements = {
                "'翼风之形": "'巽风之形",
                "'风之形": "'巽风之形",
                "'芒之形": "'锋芒之形",
                "'嘎偶之形": "'偃偶之形",
                "'優偶之形": "'偃偶之形",
                "'厦偶之形": "'偃偶之形",
                "'偶之形": "'偃偶之形",
                "'兽之形": "'孽兽之形",
                "'潘灼之形": "'燔灼之形",
                "'熠灼之形": "'燔灼之形",
                "'灼之形": "'燔灼之形",
                "'幽寞之径": "'幽冥之径",
                "'幽幂之径": "'幽冥之径",
                "'幽之径": "'幽冥之径",
                "'冥之径": "'幽冥之径",
                "'蛀星的旧履": "'蛀星的旧靥",
                "'蛀星的旧膚": "'蛀星的旧靥",
                "'蛀星的旧魔": "'蛀星的旧靥",
                "'蛀星的旧": "'蛀星的旧靥",
                "“异器盈界": "异器盈界",
                "“花藏繁生": "花藏繁生",
                "“位面分裂": "位面分裂",
                "拟造花萼 （赤)": "拟造花萼（赤）",
                "拟造花萼 （金)": "拟造花萼（金）",
                "拟造花萼 (赤)": "拟造花萼（赤）",
                "拟造花萼 (金)": "拟造花萼（金）",
                "焦灸之形": "焦炙之形",
                "集多之形": "焦炙之形",
                "怒之形": "嗔怒之形",
                "未日幻影": "末日幻影",
                "时者": "莳者"
            }

            originalStr = str(originalDict)
            for oldStr, newStr in replacements.items():
                originalStr = originalStr.replace(oldStr, newStr)

            modifiedDict = eval(originalStr)
            return modifiedDict
        except Exception as e:
            self.log.error(self.logMgr.Error(e))
            return r"{}"

    def RecognizeSingleLine(self, image, blacklist=None):
        results = self.ConvertFormat(self.Run(image))
        if results:
            for i in range(len(results)):
                lineText = results[i][1][0] if results and len(results[i]) > 0 else ""
                if blacklist and any(char == lineText for char in blacklist):
                    continue
                else:
                    return lineText, results[i][1][1]
        return None

    def RecognizeMultiLines(self, image):
        result = self.ConvertFormat(self.Run(image))
        return result
