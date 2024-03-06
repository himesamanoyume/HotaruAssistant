import numpy as np,time,math,cv2

class DetectScreenSubModule:

    def __init__(self, window_title):
        self.window_title = window_title
        self.screenshot = None
        self.InitDetectScreen()
    
    # 兼容旧代码
    @classmethod
    def InitDetectScreen(cls):
        pass
        # self.mouse_click = Input.mouse_click
        # self.mouse_down = Input.mouse_down
        # self.mouse_up = Input.mouse_up
        # self.mouse_move = Input.mouse_move
        # self.mouse_scroll = Input.mouse_scroll
        # self.press_key = Input.press_key
        # self.press_mouse = Input.press_mouse