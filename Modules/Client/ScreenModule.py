from .DetectScreenSubModule import DetectScreenSubModule
from .DevScreenSubModule import DevScreenSubModule
from .ScreenshotScreenSubModule import ScreenshotScreenSubModule
from .ResulotionScreenSubModule import ResulotionScreenSubModule

class ScreenModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mDetectScreen = DetectScreenSubModule()
            cls.mDevScreen = DevScreenSubModule()
            cls.mScreenshot = ScreenshotScreenSubModule()
            cls.mResulotionScreen = ResulotionScreenSubModule()
        return cls.mInstance