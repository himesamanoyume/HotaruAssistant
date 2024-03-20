from States import *
import time, datetime

class GetPowerInfoState(BaseState):

    mStateName = 'GetPowerState'

    def OnBegin(self):
        trailblazePowerCrop = (1588.0 / 1920, 35.0 / 1080, 198.0 / 1920, 56.0 / 1080)

        if configMgr.mConfig[configMgr.mKey.USE_RESERVED_TRAILBLAZE_POWER][dataMgr.currentUid] or configMgr.mConfig[configMgr.mKey.USE_FUEL][dataMgr.currentUid]:
            screenMgr.ChangeTo('map')
            # 打开开拓力补充界面
            if screenMgr.ClickElement("./assets/images/share/trailblaze_power/trailblaze_power.png", "image", 0.9, crop=trailblazePowerCrop):
                # 等待界面加载
                if screenMgr.FindElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=10):
                    # 开启使用后备开拓力
                    if configMgr.mConfig[configMgr.mKey.USE_RESERVED_TRAILBLAZE_POWER][dataMgr.currentUid] and screenMgr.ClickElement("./assets/images/share/trailblaze_power/reserved_trailblaze_power.png", "image", 0.9, scaleRange=(0.95, 0.95)):
                        GetPowerInfoState.MoveButtonAndConfirm()
                    # 开启使用燃料
                    elif configMgr.mConfig[configMgr.mKey.USE_FUEL][dataMgr.currentUid] and screenMgr.ClickElement("./assets/images/share/trailblaze_power/fuel.png", "image", 0.9, scaleRange=(0.95, 0.95)):
                        GetPowerInfoState.MoveButtonAndConfirm()
                    # # 开启使用星琼
                    # elif config.stellar_jade and auto.click_element("./assets/images/share/trailblaze_power/stellar_jade.png", "image", 0.9, scaleRange=(0.95, 0.95)):
                    #     pass
                    else:
                        screenMgr.PressKey("esc")

        screenMgr.ChangeTo('map')
        dataMgr.currentPower = GetPowerInfoState.GetPower(trailblazePowerCrop)
        log.info(logMgr.Info(f"🟣开拓力: {dataMgr.currentPower}"))
        # Utils._content.update({'new_power':f'{dataMgr.currentPower}'})
        log.info(logMgr.Info(f"开拓力回满时间为:{GetPowerInfoState.GetFullPowerTime(dataMgr.currentPower)}"))
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
        return _datetime
    
    @staticmethod
    def MoveButtonAndConfirm():
        if screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=10):
            result = screenMgr.FindElement("./assets/images/share/trailblaze_power/button.png", "image", 0.9, maxRetries=10)
            if result:
                screenMgr.ClickElementWithPos(result, action="down")
                time.sleep(0.5)
                result = screenMgr.FindElement("./assets/images/share/trailblaze_power/plus.png", "image", 0.9)
                if result:
                    screenMgr.ClickElementWithPos(result, action="move")
                    time.sleep(0.5)
                    screenMgr.MouseUp()
                    if screenMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=10):
                        time.sleep(1)
                        screenMgr.PressKey("esc")
                        if screenMgr.CheckScreen("map"):
                            return True
        return False

    @staticmethod
    def GetPower(crop, type="trailblaze_power"):
        try:
            if type == "trailblaze_power":
                result = screenMgr.GetSingleLineText(crop=crop, blacklist=['+', '米'], maxRetries=3)
                power = int(result.replace("1240", "/240").split('/')[0])
                return power if 0 <= power <= 999 else -1
            elif type == "reserved_trailblaze_power":
                result = screenMgr.GetSingleLineText(crop=crop, blacklist=['+', '米'], maxRetries=3)
                power = int(result[0])
                return power if 0 <= power <= 2400 else -1
        except Exception as e:
            log.error(logMgr.Error(f"识别开拓力失败: {e}"))
            return -1