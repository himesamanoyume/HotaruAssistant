# from .DetectScreenSubModule import DetectScreenSubModule
# from .ScreenshotScreenSubModule import ScreenshotScreenSubModule
# from .ResulotionScreenSubModule import ResulotionScreenSubModule
from .DevScreenSubModule import DevScreenSubModule
import threading,time,json,sys
from Hotaru.Client.LogClientHotaru import logMgr,log
from collections import deque
import pyautogui,win32gui

class ScreenModule:

    def __init__(self, configPath="./assets/config/screens.json"):
        self.mDevScreen = DevScreenSubModule()
        self.currentScreen = None
        self.screenMap = {}
        self.SetupScreensFromConfig(configPath)
        self.green = "\033[92m"
        self.reset = "\033[0m"

    @staticmethod
    def SwitchToWindow(title, maxRetries, isGameWindow = True):
        for i in range(maxRetries):
            windows = pyautogui.getWindowsWithTitle(title)
            if not windows:
                continue
            for window in windows:
                if window.title == title:
                    if isGameWindow:
                        try:
                            hwnd = win32gui.FindWindow("UnityWndClass", title)
                            win32gui.GetWindowRect(hwnd)
                        except Exception as e:
                            continue
                    try:
                        window.restore()
                        window.activate()
                    except Exception as e:
                        log.warning(logMgr.Warning(e))
                    time.sleep(2)
                    if window.isActive:
                        if isGameWindow:
                            try:
                                hwnd = win32gui.FindWindow("UnityWndClass", title)
                                win32gui.GetWindowRect(hwnd)
                                return True
                            except Exception as e:
                                log.warning(logMgr.Warning(e))
                    log.warning(logMgr.Warning("切换窗口失败,尝试ALT+TAB"))
                    pyautogui.hotkey('alt', 'tab')
                    time.sleep(2)
                    continue
        return False



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
        
    # @classmethod
    # def GetName(cls, id):
    #     return cls.screenMap[id]["name"]
    
    # @classmethod
    # def FindShortestPath(cls, start, end):
    #     """
    #     在界面图中查找从 start 到 end 的最短路径
    #     :param start: 起始界面
    #     :param end: 目标界面
    #     :return: 找到的最短路径列表，如果不存在则返回 None
    #     """
    #     if start == end:
    #         return [end]

    #     visited = set()
    #     queue = deque([(start, [])])  # 每个元素为 (当前界面, 到达当前界面的路径)

    #     while queue:
    #         currentScreen, path = queue.popleft()
    #         visited.add(currentScreen)

    #         for action in cls.screenMap[currentScreen]['actions']:
    #             nextScreen = action["target_screen"]
    #             if nextScreen not in visited:
    #                 newPath = path + [currentScreen]
    #                 if nextScreen == end:
    #                     return newPath + [end]
    #                 queue.append((nextScreen, newPath))

    #     return None
    
    # @classmethod
    # def PerformOperations(cls, operations):
    #     """
    #     执行一系列操作，包括按键操作和鼠标点击操作
    #     :param operations: 操作序列，每个操作是一个元组 (函数名, 参数)
    #     """
    #     def parse_args(args):
    #         parsed_args = []
    #         kwargs = {}
    #         for arg in args:
    #             if isinstance(arg, str):
    #                 if "=" in arg:
    #                     key, value = arg.split("=")
    #                     kwargs[key] = eval(value)
    #                     continue
    #             parsed_args.append(arg)
    #         return parsed_args, kwargs

    #     for operation in operations:
    #         function_name = operation["action"]
    #         args = operation["args"]
    #         parsed_args, kwargs = parse_args(args)

    #         if hasattr(cls, function_name):
    #             func = getattr(cls, function_name)
    #             func(*parsed_args, **kwargs)
    #             logClientMgr.Debug("执行了一个操作")
    #         else:
    #             module_name, method_name = function_name.split('.')
    #             module = globals().get(module_name)
    #             if module and hasattr(module, method_name):
    #                 method = getattr(module, method_name)
    #                 method(*parsed_args, **kwargs)
    #                 logClientMgr.Debug("执行了一个操作")
    #             else:
    #                 logClientMgr.Debug(f"未知的操作: {function_name}")

    # @classmethod
    # def GetCurrentScreen(cls, autotry=True, maxRetries=5):
    #     """
    #     获取当前界面
    #     :param autotry: 未识别出任何界面自动按ESC
    #     :param maxRetries: 重试次数
    #     :return: True，如果查找失败则返回 False
    #     """
    #     pass

        # @classmethod
        # def FindScreen(cls, screen_name, screen):
        #     try:
        #         if auto.find_element(screen['image_path'], "image", 0.9, take_screenshot=False):
        #             with cls.lock:  # 使用锁来保护对共享变量的访问
        #                 cls.current_screen = screen_name
        #     except Exception as e:
        #         logger.debug(_("识别界面出错：{e}").format(e=e))

        # for i in range(maxRetries):
        #     auto.take_screenshot()
        #     cls.current_screen = None

        #     threads = []
        #     for screen_name, screen in cls.screen_map.items():
        #         thread = threading.Thread(target=FindScreen, args=(cls, screen_name, screen))
        #         threads.append(thread)
        #         thread.start()
        #     for thread in threads:
        #         thread.join()

        #     if cls.current_screen:
        #         screen_name=cls.green + cls.get_name(cls.current_screen) + cls.reset
        #         logger.info(gu(f"当前界面：{screen_name}"))
        #         if cls.get_name(cls.current_screen) == "星际和平指南-每日实训":
        #             logger.warning(gu("进入到星际和平指南-每日实训的判断"))
        #             time.sleep(0.5)
        #             if not Utils.is_next_4_am(config.last_run_timestamp, Utils.get_uid()):
        #                 while Utils.click_element_quest("./assets/images/quest/receive.png", "image", 0.9, crop=(265.0 / 1920, 394.0 / 1080, 1400.0 / 1920, 504.0 / 1080)):
        #                     time.sleep(1)
        #         elif cls.get_name(cls.current_screen) == "遗器已满":
        #             auto.relic_full_error()
        #         return True

        #     if autotry:
        #         logger.warning(gu("未识别出任何界面，请确保游戏画面干净，按ESC后重试"))
        #         auto.press_key("esc")
        #         time.sleep(1)
        #         import random
        #         auto.mouse_scroll(5, 1 + -2 * random.randint(0,1))
        #         time.sleep(0.2)
        #     else:
        #         logger.debug(gu("未识别出任何界面，请确保游戏画面干净"))
        #         break
        # logger.error(gu("当前界面：未知"))
        # return False