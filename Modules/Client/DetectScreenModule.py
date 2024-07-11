import numpy as np,time,math,cv2,os
from Hotaru.Client.LogClientHotaru import log,logMgr
from Hotaru.Client.OcrClientHotaru import ocrClientMgr
from .ClickScreenSubModule import ClickScreenSubModule
from Modules.Utils.GameWindow import GameWindow
from Hotaru.Client.DataClientHotaru import dataClientMgr
from Hotaru.Client.ConfigClientHotaru import configMgr

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
    
    def TakeSpecialScreenshot(self, crop=(0,0,0,0), isException = False):
        result = GameWindow.TakeScreenshot(crop)
        if result:
            if not os.path.exists(f"screenshots/{dataClientMgr.currentUid}"):
                os.makedirs(f"screenshots/{dataClientMgr.currentUid}")
            
            if not isException:
                pos = "daily" 
            else:
                pos = "exception"

            screenshotPath = f"{os.path.abspath('screenshots')}/{dataClientMgr.currentUid}/{pos}.png"
            self.screenshot.save(screenshotPath)
            log.debug(logMgr.Debug(f"已保存截图:{screenshotPath}"))

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
    
    def ClickElementQuest(self, target, findType, threshold=None, maxRetries=1, crop=(0, 0, 0, 0), takeScreenshot=True, relative=False, scaleRange=None, include=None, need_ocr=True, source=None, offset=(0, 0)):
        coordinates = self.FindElement(target, findType, threshold, maxRetries, crop, takeScreenshot,
                                        relative, scaleRange, include, need_ocr, source)
        if coordinates:
            log.warning(logMgr.Warning("检测到每日任务待领取"))
            return self.ClickElementWithPosQuest(coordinates, offset)
        return False
    
    def ClickElementWithPosQuest(self, coordinates, offset=(0, 0), action="click"):
        self.TakeScreenshot(crop=(297.0 / 1920, 478.0 / 1080, 246.0 / 1920, 186.0 / 1080))
        # time.sleep(2)
        result = ocrClientMgr.mOcr.RecognizeMultiLines(self.screenshot)
        result_keyword = result[0][1][0]
        # time.sleep(0.5)
        for mappingsKeyword, taskName in dataClientMgr.meta["task_mappings"].items():
            if mappingsKeyword in result_keyword:
                if taskName in configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid] and configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid][taskName] == True:
                    configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid][taskName] = False
                    log.warning(logMgr.Warning(f"keyword:{mappingsKeyword}----->{taskName}:进行了点击,任务已经完成"))
                else:
                    log.warning(logMgr.Warning(f"keyword:{mappingsKeyword}----->{taskName}:进行了点击,但可能配置项中之前已完成修改或未识别成功"))
                break
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
                time.sleep(0.1)
        return None

    def FindImageElement(self, target, threshold, scaleRange, relative=False):
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
            max_val, max_loc = self.ScaleAndMatchTemplate(screenshot, template, threshold, scaleRange)
            if threshold is None or max_val >= threshold:
                log.debug(logMgr.Debug(f"目标图片：{target} 相似度：{max_val}"))
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
                self.ocrResult = ocrClientMgr.mOcr.RecognizeMultiLines(np.array(self.screenshot))
            if not self.ocrResult:
                log.debug(logMgr.Debug(f"目标文字：{', '.join(target)} 未找到，没有识别出任何文字"))
                return None, None
            for box in self.ocrResult:
                text = box[1][0]
                # if (include is None and target == text) or (include and target in text) or (not include and target == text):
                if ((include is None or not include) and text in target) or (include and any(t in text for t in target)):
                    self.matchedText = next((t for t in target if t in text), None)
                    log.debug(logMgr.Debug(f"目标文字：{self.matchedText} 相似度：{box[1][1]}"))
                    if relative == False:
                        top_left = (box[0][0][0] + self.screenshotPos[0], box[0][0][1] + self.screenshotPos[1])
                        bottom_right = (box[0][2][0] + self.screenshotPos[0], box[0][2][1] + self.screenshotPos[1])
                    else:
                        top_left = (box[0][0][0], box[0][0][1])
                        bottom_right = (box[0][2][0], box[0][2][1])
                    return top_left, bottom_right
            log.debug(logMgr.Debug(f"目标文字：{', '.join(target)} 未找到，没有识别出匹配文字"))
            return None, None
        except Exception as e:
            log.error(logMgr.Error(f"寻找文字：{', '.join(target)} 出错：{e}"))
            return None, None

    def FindMinDistanceTextElement(self, target, source, sourceType, include, needOcr=True):
        if needOcr:
            self.ocrResult = ocrClientMgr.mOcr.RecognizeMultiLines(np.array(self.screenshot))

        sourcePos = None
        if sourceType == 'text':
            if not self.ocrResult:
                log.debug(logMgr.Debug(f"目标文字：{source} 未找到，没有识别出任何文字"))
                return None, None
            log.debug(logMgr.Debug(self.ocrResult))
            for box in self.ocrResult:
                text = box[1][0]
                if ((include is None or not include) and source == text) or (include and source in text):
                    log.debug(logMgr.Debug(f"目标文字：{source} 相似度：{box[1][1]}"))
                    sourcePos = box[0][0]
                    break
        elif sourceType == 'image':
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
        minDistance = float('inf')
        for box in self.ocrResult:
            text = box[1][0]
            if ((include is None or not include) and text in target) or (include and any(t in text for t in target)):
                matchedText = next((t for t in target if t in text), None)
                pos = box[0]
                # 如果target不在source右下角
                if not ((pos[0][0] - sourcePos[0]) > 0 and (pos[0][1] - sourcePos[1]) > 0):
                    continue
                distance = math.sqrt((pos[0][0] - sourcePos[0]) **
                                     2 + (pos[0][1] - sourcePos[1]) ** 2)
                log.debug(logMgr.Debug(f"目标文字：{matchedText} 相似度：{box[1][1]} 距离：{distance}"))
                if distance < minDistance:
                    minTarget = matchedText
                    minDistance = distance
                    targetPos = pos
        if targetPos is None:
            log.debug(logMgr.Debug(f"目标文字：{', '.join(target)} 未找到，没有识别出匹配文字"))
            return None, None
        log.debug(logMgr.Debug(f"目标文字：{minTarget} 最短距离：{minDistance}"))
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

    def ClickElement(self, target, findType, threshold=None, maxRetries=5, crop=(0, 0, 0, 0), takeScreenshot=True, relative=False, scaleRange=None, include=None, needOcr=True, source=None, sourceType=None, offset=(0, 0), isLog=False):
        coordinates = self.FindElement(target, findType, threshold, maxRetries, crop, takeScreenshot,
                                        relative, scaleRange, include, needOcr, source, sourceType)
        if coordinates:
            if isLog:
                log.info(logMgr.Info(f"成功找到目标"))
            return self.ClickElementWithPos(coordinates, offset)
        if isLog:
            log.warning(logMgr.Warning(f"未找到目标!"))
        return False

    def GetSingleLineText(self, crop=(0, 0, 0, 0), blacklist=None, maxRetries=5):
        for i in range(maxRetries):
            self.screenshot, self.screenshotPos = self.TakeScreenshot(crop)
            ocrResult = ocrClientMgr.mOcr.RecognizeSingleLine(np.array(self.screenshot), blacklist)
            if ocrResult:
                return ocrResult[0]
        return None
    