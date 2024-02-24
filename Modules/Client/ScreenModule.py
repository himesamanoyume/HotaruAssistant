from Modules.Client.DetectScreenSubModule import DetectScreenSubModule
from Modules.Client.DevScreenSubModule import DevScreenSubModule
from Modules.Client.ScreenshotScreenSubModule import ScreenshotScreenSubModule
from Modules.Client.ResulotionScreenSubModule import ResulotionScreenSubModule

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