from States.Client import *
import time, datetime

class GetPowerInfoState(BaseClientState):

    mStateName = 'GetPowerInfoState'

    def OnBegin(self):
        trailblazePowerCrop = (1588.0 / 1920, 35.0 / 1080, 198.0 / 1920, 56.0 / 1080)

        if configMgr.mConfig[configMgr.mKey.USE_RESERVED_TRAILBLAZE_POWER][dataClientMgr.currentUid] or configMgr.mConfig[configMgr.mKey.USE_FUEL][dataClientMgr.currentUid]:
            screenClientMgr.ChangeTo('map')
            # 打开开拓力补充界面
            if screenClientMgr.ClickElement("./assets/static/images/share/trailblaze_power/trailblaze_power.png", "image", 0.9, crop=trailblazePowerCrop):
                # 等待界面加载
                if screenClientMgr.FindElement("./assets/static/images/base/confirm.png", "image", 0.9, maxRetries=3):
                    # 开启使用后备开拓力
                    if configMgr.mConfig[configMgr.mKey.USE_RESERVED_TRAILBLAZE_POWER][dataClientMgr.currentUid] and screenClientMgr.ClickElement("./assets/static/images/share/trailblaze_power/reserved_trailblaze_power.png", "image", 0.9, scaleRange=(0.95, 0.95)):
                        self.MoveButtonAndConfirm()
                    # 开启使用燃料
                    elif configMgr.mConfig[configMgr.mKey.USE_FUEL][dataClientMgr.currentUid] and screenClientMgr.ClickElement("./assets/static/images/share/trailblaze_power/fuel.png", "image", 0.9, scaleRange=(0.95, 0.95)):
                        self.MoveButtonAndConfirm()
                    # # 开启使用星琼
                    # elif config.stellar_jade and auto.click_element("./assets/static/images/share/trailblaze_power/stellar_jade.png", "image", 0.9, scaleRange=(0.95, 0.95)):
                    #     pass
                    else:
                        screenClientMgr.PressKey("esc")

        screenClientMgr.ChangeTo('map')
        dataClientMgr.currentPower = self.GetPower(trailblazePowerCrop)
        log.info(logMgr.Info(f"🟣开拓力: {dataClientMgr.currentPower}"))
        # Utils._content.update({'new_power':f'{dataMgr.currentPower}'})
        log.info(logMgr.Info(f"开拓力回满时间为:{self.GetFullPowerTime(dataClientMgr.currentPower)}"))
        # Utils._content.update({'full_power_time':f'{Utils.getFullPowerTime(dataMgr.currentPower)}'})

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    @staticmethod
    def GetFullPowerTime(power):
        remainingPower = 240 - power
        timestamp = remainingPower * 360 + time.time()
        _datetime = datetime.datetime.fromtimestamp(timestamp)
        dataClientMgr.notifyContent["开拓力回满时间"] = _datetime
        return _datetime
    
    @staticmethod
    def MoveButtonAndConfirm():
        if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
            result = screenClientMgr.FindElement("./assets/static/images/share/trailblaze_power/button.png", "image", 0.9)
            if result:
                screenClientMgr.ClickElementWithPos(result, action="down")
                result = screenClientMgr.FindElement("./assets/static/images/share/trailblaze_power/plus.png", "image", 0.9)
                if result:
                    screenClientMgr.ClickElementWithPos(result, action="move")
                    screenClientMgr.MouseUp()
                    if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                        screenClientMgr.PressKey("esc")
                        if screenClientMgr.CheckScreen("map"):
                            return True
        return False

    @staticmethod
    def GetPower(crop, type="trailblaze_power"):
        try:
            if type == "trailblaze_power":
                result = screenClientMgr.GetSingleLineText(crop=crop, blacklist=['+', '米'])
                power = int(result.replace("1240", "/240").split('/')[0])
                return power if 0 <= power <= 999 else -1
            elif type == "reserved_trailblaze_power":
                result = screenClientMgr.GetSingleLineText(crop=crop, blacklist=['+', '米'])
                power = int(result[0])
                return power if 0 <= power <= 2400 else -1
        except Exception as e:
            log.error(logMgr.Error(f"识别开拓力失败: {e}"))
            return -1