# from .DetectScreenSubModule import DetectScreenSubModule
# from .ScreenshotScreenSubModule import ScreenshotScreenSubModule
# from .ResulotionScreenSubModule import ResulotionScreenSubModule
from Hotaru.Client.ConfigClientHotaru import configMgr
from .DetectDevScreenSubModule import DetectDevScreenSubModule
from .DetectScreenModule import DetectScreenModule
from Hotaru.Client.LogClientHotaru import logMgr,log
from collections import deque
from Modules.Utils.GameWindow import GameWindow
import threading,time,json,sys,win32gui

class ScreenModule:

    def __init__(self, configPath="./assets/config/screens.json"):
        self.mDevScreen = DetectDevScreenSubModule()
        self.mDetect = DetectScreenModule(configMgr.mKey.GAME_TITLE_NAME)
        self.currentScreen = None
        self.screenMap = {}
        self.lock = threading.Lock()  # 创建一个锁，用于线程同步
        self.SetupScreensFromConfig(configPath)
        self.green = "\033[92m"
        self.reset = "\033[0m"
    
    def StartDevScreen(self):
        if configMgr.mConfig[configMgr.mKey.DEV_SCREEN_ENABLE]:
            log.info(logMgr.Info("DevScreen正在开启"))
            while True:
                window = GameWindow.GetWindow(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME])
                if not window is False:
                    if window.title in ["崩坏：星穹铁道"]:
                        self.mDevScreen.InitDevScreenLoop(window)
                    else:
                        log.warning(logMgr.Warning("未获取到游戏窗口,DevScreen无法开启"))
                
                print("等待窗口...")
                time.sleep(5)
        else:
            log.info(logMgr.Info("DevScreen配置未启用"))

    def CheckAndSwitch(self, title):
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
            function_name = operation["action"]
            args = operation["args"]
            parsed_args, kwargs = ParseArgs(args)

            if hasattr(self, function_name):
                func = getattr(self, function_name)
                func(*parsed_args, **kwargs)
                log.debug(logMgr.Debug("执行了一个操作"))
            else:
                module_name, method_name = function_name.split('.')
                module = globals().get(module_name)
                if module and hasattr(module, method_name):
                    method = getattr(module, method_name)
                    method(*parsed_args, **kwargs)
                    log.debug(logMgr.Debug("执行了一个操作"))
                else:
                    log.debug(logMgr.Debug(f"未知的操作: {function_name}"))

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