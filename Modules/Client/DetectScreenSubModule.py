import numpy as np,time,math,cv2

class DetectScreenSubModule:

    mInstance = None

    def __new__(cls, window_title):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.window_title = window_title
            cls.screenshot = None
            cls.mInstance.InitDetectScreen()

        return cls.mInstance
    
    # 兼容旧代码
    def InitDetectScreen(self):
        self.mouse_click = Input.mouse_click
        self.mouse_down = Input.mouse_down
        self.mouse_up = Input.mouse_up
        self.mouse_move = Input.mouse_move
        self.mouse_scroll = Input.mouse_scroll
        self.press_key = Input.press_key
        self.press_mouse = Input.press_mouse