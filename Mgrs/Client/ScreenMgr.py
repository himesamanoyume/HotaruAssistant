from Hotaru.Client.LogClientHotaru import logMgr,log
from Hotaru.Client.ConfigClientHotaru import configMgr
from Modules.Client.ScreenModule import ScreenModule
from Modules.Utils.Retry import Retry
import threading,time,json,sys,win32gui,threading
from Modules.Utils.GameWindow import GameWindow
from collections import deque

class ScreenMgr:
    
    def __init__(self, configPath="./assets/config/screens.json"):
        self.mScreen = ScreenModule()
        self.mDetect = self.mScreen.mDetect
        self.mDevScreen = self.mScreen.mDevScreen
        self.currentScreen = None
        self.screenMap = {}
        self.lock = threading.Lock()  # 创建一个锁，用于线程同步
        self.SetupScreensFromConfig(configPath)
        self.green = "\033[92m"
        self.reset = "\033[0m"

    def GetSingleLineText(self, crop=(0, 0, 0, 0), blacklist=None, maxRetries=3):
        """ 这种老是忘记return结果 """
        t = threading.Thread(target=self.ShowDetectArea(crop))
        t.start()
        return self.mDetect.GetSingleLineText(crop, blacklist, maxRetries)

    def FindElement(self, target, findType, threshold=None, maxRetries=1, crop=(0, 0, 0, 0), takeScreenshot=True, relative=False, scaleRange=None, include=None, needOcr=True, source=None, sourceType=None, pixelBgr=None):
        """ 这种老是忘记return结果 """
        t = threading.Thread(target=self.ShowDetectArea(crop))
        t.start()
        return self.mDetect.FindElement(target, findType, threshold, maxRetries, crop, takeScreenshot, relative, scaleRange, include, needOcr, source, sourceType, pixelBgr)
    
    def ClickElement(self, target, find_type, threshold=None, max_retries=1, crop=(0, 0, 0, 0), take_screenshot=True, relative=False, scale_range=None, include=None, need_ocr=True, source=None, source_type=None, offset=(0, 0), isLog=False):
        """ 这种老是忘记return结果 """
        t = threading.Thread(target=self.ShowDetectArea(crop))
        t.start()
        return self.mDetect.ClickElement(target, find_type, threshold, max_retries, crop, take_screenshot, relative, scale_range, include, need_ocr, source, source_type, offset, isLog)
    
    def MouseClick(self,x,y):
        self.mDetect.mouseClick(x,y)

    def MouseDown(self, x, y):
        self.mDetect.mouseDown(x, y)

    def MouseUp(self):
        self.mDetect.mouseUp()

    def MouseMove(self, x, y):
        self.mDetect.mouseMove(x, y)

    def MouseScroll(self, count, direction=-1):
        self.mDetect.mouseScroll(count, direction)

    def PressKey(self, key, wait_time=0.2):
        self.mDetect.pressKey(key, wait_time)

    def PressMouse(self, wait_time=0.2):
        self.mDetect.pressMouse(wait_time)
    
    def StartDevScreen(self):
        self.mScreen.StartDevScreen()

    def ShowDetectArea(self, detectArea):
        if self.mDevScreen.isDevScreenRunning:
            self.mDevScreen.canvas.delete('all')
            Retry.Re(lambda: self.mDevScreen.ShowDetectArea(detectArea), 2)
            self.mDevScreen.canvas.delete('all')

    @staticmethod
    def CheckAndSwitch(title):
        return GameWindow.SwitchToWindow(title, maxRetries=4)
    
    @staticmethod
    def CheckResulotion(title, width, height):
        hwnd = win32gui.FindWindow("UnityWndClass", title)
        x, y, w, h = win32gui.GetClientRect(hwnd)
        if w != width or h != height:
            log.error(logMgr.Error(f"游戏分辨率 {w}*{h} 请在游戏设置内切换为 {width}*{height} 窗口或全屏运行"))
            input("按回车键关闭窗口. . .")
            sys.exit(1)
        else:
            log.debug(logMgr.Debug(f"游戏分辨率 {w}*{h}"))

    def AddScreen(self, id, name, imagePath, actions):
            """
            添加一个新界面到界面管理器，并指定其识别图片路径、可切换的目标界面及操作序列
            :param id: 新界面的唯一标识
            :param name: 新界面的名称
            :param imagePath: 用于识别界面的图片路径
            :param actions: 可切换的目标界面及操作序列
            """
            self.screenMap[id] = {'name': name, 'image_path': imagePath, 'actions': actions}
    
    def SetupScreensFromConfig(self, configPath):
        """
        从配置文件路径中获取界面配置信息，并添加到界面管理器
        :param configPath: 配置文件路径
        """

        try:
            with open(configPath, 'r', encoding='utf-8') as file:
                for config in json.load(file):
                    id = config["id"]
                    name = config["name"]
                    imagePath = config["image_path"]
                    actions = config["actions"]
                    self.AddScreen(id, name, imagePath, actions)
        except FileNotFoundError:
            nowtime = time.time()
            logMgr.Error(f"{nowtime}配置文件不存在：{configPath}")
            raise Exception (f"{nowtime},配置文件不存在：{configPath}")
            # input(_("按回车键关闭窗口. . ."))
            # sys.exit(1)
        except Exception as e:
            nowtime = time.time()
            logMgr.Error(f"{nowtime},配置文件解析失败：{e}")
            raise Exception (f"{nowtime},配置文件解析失败：{e}")
            # input(_("按回车键关闭窗口. . ."))
            # sys.exit(1)
        
    def GetName(self, id):
        return self.screenMap[id]["name"]
    
    def FindShortestPath(self, start, end):
        """
        在界面图中查找从 start 到 end 的最短路径
        :param start: 起始界面
        :param end: 目标界面
        :return: 找到的最短路径列表，如果不存在则返回 None
        """
        if start == end:
            return [end]

        visited = set()
        queue = deque([(start, [])])  # 每个元素为 (当前界面, 到达当前界面的路径)

        while queue:
            currentScreen, path = queue.popleft()
            visited.add(currentScreen)

            for action in self.screenMap[currentScreen]['actions']:
                nextScreen = action["target_screen"]
                if nextScreen not in visited:
                    newPath = path + [currentScreen]
                    if nextScreen == end:
                        return newPath + [end]
                    queue.append((nextScreen, newPath))

        return None
    
    def PerformOperations(self, operations):
        """
        执行一系列操作，包括按键操作和鼠标点击操作
        :param operations: 操作序列，每个操作是一个元组 (函数名, 参数)
        """
        def ParseArgs(args):
            parsed_args = []
            kwargs = {}
            for arg in args:
                if isinstance(arg, str):
                    if "=" in arg:
                        key, value = arg.split("=")
                        kwargs[key] = eval(value)
                        continue
                parsed_args.append(arg)
            return parsed_args, kwargs

        for operation in operations:
            functionName = operation["action"]
            args = operation["args"]
            parsed_args, kwargs = ParseArgs(args)

            if hasattr(self, functionName):
                func = getattr(self, functionName)
                func(*parsed_args, **kwargs)
                # log.info(logMgr.Info(f"执行了一个操作: {func}"))
            else:
                moduleName, methodName = functionName.split('.')
                module = globals().get(moduleName)
                if module and hasattr(module, methodName):
                    method = getattr(module, methodName)
                    method(*parsed_args, **kwargs)
                    # log.info(logMgr.Info(f"执行了一个操作: {functionName}"))
                else:
                    log.warning(logMgr.Warning(f"未知的操作: {functionName}"))

    def FindScreen(self, screenName, screen):
            try:
                if self.mDetect.FindElement(screen['image_path'], "image", 0.9, takeScreenshot=False):
                    with self.lock:  # 使用锁来保护对共享变量的访问
                        self.currentScreen = screenName
            except Exception as e:
                log.debug(logMgr.Debug(f"识别界面出错：{e}"))

    def GetCurrentScreen(self, autotry=True, maxRetries=5):
        """
        获取当前界面
        :param autotry: 未识别出任何界面自动按ESC
        :param maxRetries: 重试次数
        :return: True，如果查找失败则返回 False
        """

        for i in range(maxRetries):
            self.mDetect.TakeScreenshot()
            self.currentScreen = None

            threads = []
            for screenName, screen in self.screenMap.items():
                thread = threading.Thread(target=self.FindScreen, args=(screenName, screen))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

            if self.currentScreen:
                screenName=self.green + self.GetName(self.currentScreen) + self.reset
                log.info(logMgr.Info(f"当前界面：{screenName}"))
                return True

            if autotry:
                log.warning(logMgr.Warning("未识别出任何界面，请确保游戏画面干净，按ESC后重试"))
                self.mDetect.pressKey("esc")
                time.sleep(1)
                import random
                self.mDetect.mouseScroll(5, 1 + -2 * random.randint(0,1))
                time.sleep(0.2)
            else:
                log.debug(logMgr.Debug("未识别出任何界面，请确保游戏画面干净"))
                break
        log.error(logMgr.Error("当前界面：未知"))
        return False
    
    def CheckScreen(self, targetScreen):
        if self.mDetect.FindElement(self.screenMap[targetScreen]['image_path'], "image", 0.9):
            self.currentScreen = targetScreen
            return True
        return False

    def ChangeTo(self, targetScreen, maxRecursion=2):
        """
        切换到目标界面，，如果失败则退出进程
        :param targetScreen: 目标界面
        :param maxRecursion: 重试次数
        """
        if self.CheckScreen(targetScreen):
            log.debug(logMgr.Debug(f"已经在 {self.GetName(targetScreen)} 界面"))
            return

        if not self.GetCurrentScreen():
            nowtime = time.time()
            log.info(logMgr.Info(f"{nowtime},请确保游戏画面干净，关闭帧率监控HUD、网速监控等一切可能影响游戏界面截图的组件"))
            log.info(logMgr.Info("如果是多显示器，游戏需要放在主显示器运行，且不支持HDR"))
            raise Exception (f"{nowtime},检测画面失败")
            # input(_("按回车键关闭窗口. . ."))
            # sys.exit(1)

        path = self.FindShortestPath(self.currentScreen, targetScreen)
        if path:
            for i in range(len(path) - 1):
                currentScreen = path[i]
                nextScreen = path[i + 1]
                operations = [action["actions_list"]
                              for action in self.screenMap[currentScreen]['actions']
                              if action["target_screen"] == nextScreen][0]
                self.PerformOperations(operations)
                for i in range(20):
                    log.debug(logMgr.Debug(f"等待：{self.GetName(nextScreen)}"))
                    if self.CheckScreen(nextScreen):
                        break
                    else:
                        time.sleep(1)

                if self.currentScreen != nextScreen:
                    if maxRecursion > 0:
                        log.warning(logMgr.Warning(f"切换到 {self.GetName(nextScreen)} 超时，准备重试"))
                        self.ChangeTo(nextScreen, maxRecursion=maxRecursion - 1)
                    else:
                        nowtime = time.time()
                        log.error(logMgr.Error(f"{nowtime},无法切换到 {self.GetName(nextScreen)},请确保你的账号已经解锁该功能,且不要在配置中选择你未解锁的副本或功能"))
                        log.info(logMgr.Info("请确保游戏画面干净，关闭帧率监控HUD、网速监控等一切可能影响游戏界面截图的组件"))
                        log.info(logMgr.Info("如果是多显示器，游戏需要放在主显示器运行，且不支持HDR"))
                        raise Exception (f"{nowtime},无法切换到 {self.GetName(nextScreen)},请确保你的账号已经解锁该功能,且不要在配置中选择你未解锁的副本或功能")
                        # input(_("按回车键关闭窗口. . ."))
                        # sys.exit(1)

                
                log.info(logMgr.Info(f"切换到：{self.green + self.GetName(nextScreen) + self.reset}"))
                time.sleep(1)
            self.currentScreen = targetScreen  # 更新当前界面
            return

        log.debug(logMgr.Debug(f"无法从 {self.GetName(self.currentScreen)} 切换到 {self.GetName(targetScreen)}"))
        nowtime = time.time()
        log.error(logMgr.Error(f"{nowtime},无法从 {self.GetName(self.currentScreen)} 切换到 {self.GetName(targetScreen)}"))
        raise Exception (f"{nowtime},无法从 {self.GetName(self.currentScreen)} 切换到 {self.GetName(targetScreen)}")
        # input(_("按回车键关闭窗口. . ."))
        # sys.exit(1)
