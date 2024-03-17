import numpy as np,time,math,cv2
from Hotaru.Client.LogClientHotaru import log,logMgr
# from .OcrModule import OcrModule
from Hotaru.Client.OcrHotaru import ocrMgr
from Modules.Utils.Retry import Retry
from .DetectDevScreenSubModule import DetectDevScreenSubModule
from .ClickScreenSubModule import ClickScreenSubModule
from Modules.Utils.GameWindow import GameWindow

class DetectScreenModule:

    def __init__(self, windowTitle):
        self.windowTitle = windowTitle
        self.screenshot = None
        self.InitClickModule()

    def InitClickModule(self):
        self.mouseClick = ClickScreenSubModule.MouseClick
        self.mouseDown = ClickScreenSubModule.MouseDown
        self.mouseUp = ClickScreenSubModule.MouseUp
        self.mouseMove = ClickScreenSubModule.MouseMove
        self.mouseScroll = ClickScreenSubModule.MouseScroll
        self.pressKey = ClickScreenSubModule.PressKey
        self.pressMouse = ClickScreenSubModule.PressMouse

    def TakeScreenshot(self, crop=(0, 0, 0, 0)):
        result = GameWindow.TakeScreenshot(crop)
        if result:
            self.screenshot, self.screenshotPos = result
        return result

    def GetImageInfo(self, image_path):
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        return template.shape[::-1]

    def ScaleAndMatchTemplate(self, screenshot, template, threshold=None, scaleRange=None):
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if (threshold is None or max_val < threshold) and scaleRange is not None:
            for scale in np.arange(scaleRange[0], scaleRange[1] + 0.0001, 0.05):
                scaled_template = cv2.resize(template, None, fx=scale, fy=scale)
                result = cv2.matchTemplate(screenshot, scaled_template, cv2.TM_CCOEFF_NORMED)
                _, local_max_val, _, local_max_loc = cv2.minMaxLoc(result)

                if local_max_val > max_val:
                    max_val = local_max_val
                    max_loc = local_max_loc

        return max_val, max_loc
    
    def FindElement(self, target, findType, threshold=None, maxRetries=1, crop=(0, 0, 0, 0), takeScreenshot=True, relative=False, scaleRange=None, include=None, needOcr=True, source=None, sourceType=None, pixelBgr=None):
        # 参数有些太多了，以后改
        takeScreenshot = False if not needOcr else takeScreenshot
        maxRetries = 1 if not takeScreenshot else maxRetries
        for i in range(maxRetries):
            if takeScreenshot and not self.TakeScreenshot(crop):
                continue
            if findType in ['image', 'text', "min_distance_text"]:
                if findType == 'image':
                    top_left, bottom_right = self.FindImageElement(
                        target, threshold, scaleRange, relative)
                elif findType == 'text':
                    top_left, bottom_right = self.FindTextElement(target, include, needOcr, relative)
                elif findType == 'min_distance_text':
                    top_left, bottom_right = self.FindMinDistanceTextElement(target, source, sourceType, include, needOcr)
                if top_left and bottom_right:
                    return top_left, bottom_right
            elif findType in ['image_count']:
                return self.FindImageAndCount(target, threshold, pixelBgr)
            else:
                raise ValueError("错误的类型")

            if i < maxRetries - 1:
                time.sleep(1)
        return None

    def FindImageElement(self, target, threshold, scale_range, relative=False):
        try:
            # template = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
            template = cv2.imread(target)
            if template is None:
                raise ValueError("读取图片失败")
            # screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2GRAY)
            if self.screenshot is None:
                log.error(logMgr.Error("截图为None"))
                return
            screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2RGB)
            max_val, max_loc = self.ScaleAndMatchTemplate(screenshot, template, threshold, scale_range)
            log.debug(logMgr.Debug(f"目标图片：{target} 相似度：{max_val}"))
            if threshold is None or max_val >= threshold:
                channels, width, height = template.shape[::-1]
                if relative == False:
                    top_left = (max_loc[0] + self.screenshotPos[0],
                                max_loc[1] + self.screenshotPos[1])
                else:
                    top_left = (max_loc[0], max_loc[1])
                bottom_right = (top_left[0] + width, top_left[1] + height)
                return top_left, bottom_right
        except Exception as e:
            log.error(logMgr.Error(f"寻找图片出错：{e}"))
        return None, None

    @staticmethod
    def Intersected(top_left1, botton_right1, top_left2, botton_right2):
        if top_left1[0] > botton_right2[0] or top_left2[0] > botton_right1[0]:
            return False
        if top_left1[1] > botton_right2[1] or top_left2[1] > botton_right1[1]:
            return False
        return True

    @staticmethod
    def CountTemplateMatches(target, template, threshold):
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        match_count = 0
        matches = []
        width, height = template.shape[::-1]
        for top_left in zip(*locations[::-1]):
            flag = True
            for match_top_left in matches:
                botton_right = (top_left[0] + width, top_left[1] + height)
                match_botton_right = (match_top_left[0] + width, match_top_left[1] + height)
                is_intersected = DetectScreenModule.Intersected(top_left, botton_right, match_top_left, match_botton_right)
                if is_intersected:
                    flag = False
                    break
            if flag == True:
                matches.append(top_left)
                match_count += 1
        return match_count

    def FindImageAndCount(self, target, threshold, pixelBgr):
        try:
            template = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
            screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_BGR2RGB)
            bw_map = np.zeros(screenshot.shape[:2], dtype=np.uint8)
            # 遍历每个像素并判断与目标像素的相似性
            bw_map[np.sum((screenshot - pixelBgr) ** 2, axis=-1) <= 800] = 255
            return DetectScreenModule.CountTemplateMatches(bw_map, template, threshold)
        except Exception as e:
            log.error(logMgr.Error(f"寻找图片并计数出错：{e}"))
            return None

    def FindTextElement(self, target, include, needOcr=True, relative=False):
        # 兼容旧代码
        if isinstance(target, str):
            target = (target,)
        try:
            if needOcr:
                self.ocrResult = ocrMgr.mOcr.RecognizeMultiLines(np.array(self.screenshot))
            if not self.ocrResult:
                log.debug(logMgr.Debug(f"目标文字：{', '.join(target)} 未找到，没有识别出任何文字"))
                return None, None
            for box in self.ocrResult:
                text = box[1][0]
                # if (include is None and target == text) or (include and target in text) or (not include and target == text):
                if ((include is None or not include) and text in target) or (include and any(t in text for t in target)):
                    self.matchedText = next((t for t in target if t in text), None)
                    log.debug(logMgr.Debug("目标文字：{target} 相似度：{max_val}").format(target=self.matchedText, max_val=box[1][1]))
                    if relative == False:
                        top_left = (box[0][0][0] + self.screenshotPos[0], box[0][0][1] + self.screenshotPos[1])
                        bottom_right = (box[0][2][0] + self.screenshotPos[0], box[0][2][1] + self.screenshotPos[1])
                    else:
                        top_left = (box[0][0][0], box[0][0][1])
                        bottom_right = (box[0][2][0], box[0][2][1])
                    return top_left, bottom_right
            log.debug(logMgr.Debug("目标文字：{target} 未找到，没有识别出匹配文字").format(target=", ".join(target)))
            return None, None
        except Exception as e:
            log.error(logMgr.Error("寻找文字：{target} 出错：{e}").format(target=", ".join(target), e=e))
            return None, None

    def FindMinDistanceTextElement(self, target, source, source_type, include, need_ocr=True):
        if need_ocr:
            self.ocrResult = ocrMgr.mOcr.RecognizeMultiLines(np.array(self.screenshot))

        sourcePos = None
        if source_type == 'text':
            if not self.ocrResult:
                log.debug(logMgr.Debug(f"目标文字：{source} 未找到，没有识别出任何文字"))
                return None, None
            # log.debug(self.ocr_result)
            for box in self.ocrResult:
                text = box[1][0]
                if ((include is None or not include) and source == text) or (include and source in text):
                    log.debug(logMgr.Debug("目标文字：{source} 相似度：{maxVal}").format(
                        source=source, maxVal=box[1][1]))
                    sourcePos = box[0][0]
                    break
        elif source_type == 'image':
            sourcePos, i = self.FindImageElement(source, 0.9, None, True)

        if sourcePos is None:
            log.debug(logMgr.Debug(f"目标内容：{source} 未找到"))
            return None, None
        else:
            log.debug(logMgr.Debug(f"目标内容：{source} 坐标：{sourcePos}"))

        # 兼容旧代码
        if isinstance(target, str):
            target = (target,)
        targetPos = None
        min_distance = float('inf')
        for box in self.ocrResult:
            text = box[1][0]
            if ((include is None or not include) and text in target) or (include and any(t in text for t in target)):
                matched_text = next((t for t in target if t in text), None)
                pos = box[0]
                # 如果target不在source右下角
                if not ((pos[0][0] - sourcePos[0]) > 0 and (pos[0][1] - sourcePos[1]) > 0):
                    continue
                distance = math.sqrt((pos[0][0] - sourcePos[0]) **
                                     2 + (pos[0][1] - sourcePos[1]) ** 2)
                log.debug(logMgr.Debug("目标文字：{target} 相似度：{max_val} 距离：{min_distance}").format(target=matched_text, max_val=box[1][1], min_distance=distance))
                if distance < min_distance:
                    min_target = matched_text
                    min_distance = distance
                    targetPos = pos
        if targetPos is None:
            log.debug(logMgr.Debug("目标文字：{target} 未找到，没有识别出匹配文字").format(target=", ".join(target)))
            return None, None
        log.debug(logMgr.Debug("目标文字：{target} 最短距离：{min_distance}").format(target=min_target, min_distance=min_distance))
        top_left = (targetPos[0][0] + self.screenshotPos[0], targetPos[0][1] + self.screenshotPos[1])
        bottom_right = (targetPos[2][0] + self.screenshotPos[0], targetPos[2][1] + self.screenshotPos[1])
        return top_left, bottom_right

    def ClickElementWithPos(self, coordinates, offset=(0, 0), action="click"):
        (left, top), (right, bottom) = coordinates
        x = (left + right) // 2 + offset[0]
        y = (top + bottom) // 2 + offset[1]
        if action == "click":
            self.mouseClick(x, y)
        elif action == "down":
            self.mouseDown(x, y)
        elif action == "move":
            self.mouseMove(x, y)
        return True

    def ClickElement(self, target, findType, threshold=None, maxRetries=1, crop=(0, 0, 0, 0), takeScreenshot=True, relative=False, scaleRange=None, include=None, needOcr=True, source=None, sourceType=None, offset=(0, 0), isLog=False):
        coordinates = self.FindElement(target, findType, threshold, maxRetries, crop, takeScreenshot,
                                        relative, scaleRange, include, needOcr, source, sourceType)
        if coordinates:
            if isLog:
                log.info(logMgr.Info(f"成功找到目标"))
            return self.ClickElementWithPos(coordinates, offset)
        if isLog:
            log.warning(logMgr.Warning(f"未找到目标!"))
        return False

    def GetSingleLineText(self, crop=(0, 0, 0, 0), blacklist=None, maxRetries=3):
        for i in range(maxRetries):
            self.screenshot, self.screenshotPos = self.TakeScreenshot(crop)
            ocrResult = ocrMgr.mOcr.RecognizeSingleLine(np.array(self.screenshot), blacklist)
            if ocrResult:
                return ocrResult[0]
        return None
    