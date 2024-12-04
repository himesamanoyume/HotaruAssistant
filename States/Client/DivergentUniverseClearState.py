from States.Client import *
from .BaseUniverseState import BaseUniverseState
from Modules.Utils.Command import Command
import math

class DivergentUniverseClearState(BaseUniverseState):

    """
    OnBegin(), OnRunning()的返回值为True时, 代表状态将在此处结束, 不进行OnExit()以外的后续流程
    """

    mStateName = 'DivergentUniverseClearState'

    def OnBegin(self):
        currentScore, maxScore = configMgr.mConfig[configMgr.mKey.UNIVERSE_SCORE][dataClientMgr.currentUid].split('/')
        if int(currentScore) < int(maxScore):
            screenClientMgr.ChangeTo('main')

            log.info(logMgr.Info("开始校准"))
            if Command.SubprocessWithTimeout([configMgr.mConfig[configMgr.mKey.VENV_EXE_PATH], "align_angle.py"], 60, configMgr.mConfig[configMgr.mKey.UNIVERSE_PATH], configMgr.env):
                
                screenClientMgr.ChangeTo('guide5')
                log.info(logMgr.Info("开始差分宇宙"))
            else:
                log.error(logMgr.Error("校准失败"))
                return True
        else:
            log.info(logMgr.Info("当前积分已满,跳过差分宇宙"))
            return False

    def OnRunning(self):
        return self.RunDivergentUniverse() 

    def OnExit(self):
        return False
    
    def RunDivergentUniverse(self):
        log.info(logMgr.Info("进入到执行差分宇宙部分"))
        command = [configMgr.mConfig[configMgr.mKey.VENV_EXE_PATH], "diver.py"]

        if not dataClientMgr.currentUniverseScore < dataClientMgr.maxCurrentUniverseScore:
            log.debug(logMgr.Debug(f"当前积分:{dataClientMgr.currentUniverseScore},最大积分:{dataClientMgr.maxCurrentUniverseScore}"))
            log.info(logMgr.Info("鉴定为分数已满,跳过"))
            return True
            
        self.SelectUniverse()

        if dataClientMgr.currentUniverseScore == 0:
            log.info(logMgr.Info("积分为0,鉴定为首次进行差分宇宙"))
        elif dataClientMgr.currentUniverseScore == dataClientMgr.maxCurrentUniverseScore:
            log.info(logMgr.Info("积分为最大积分,鉴定为完成周常后额外进行差分宇宙"))
        else:
            log.info(logMgr.Info("积分不为0也不为最大积分,鉴定为不是首次进行差分宇宙"))
            
        if configMgr.mConfig[configMgr.mKey.UNIVERSE_SPEED_ENABLE][dataClientMgr.currentUid]:
            command.append("--speed")
        
        command.append(f"--nums=1")
            
        # end
        log.info(logMgr.Info("将开始进行差分宇宙"))        
        if Command.SubprocessWithTimeout(command, configMgr.mConfig[configMgr.mKey.UNIVERSE_TIMEOUT] * 3600, configMgr.mConfig[configMgr.mKey.UNIVERSE_PATH], configMgr.env):

            log.info(logMgr.Info("🎉差分宇宙已完成1次🎉"))
            dataClientMgr.notifyContent["副本情况"]["差分宇宙"] += 1
        
            screenClientMgr.ChangeTo('main')
            # 此时保存运行的时间戳
            configMgr.SaveTimestampByUid(configMgr.mKey.UNIVERSE_TIMESTAMP, dataClientMgr.currentUid)
            # end

            # 此时领取积分奖励
            log.info(logMgr.Info("尝试领取一遍积分奖励"))
            self.GetUniverseReward()
            # end
            
            return False
        else:
            log.error(logMgr.Error("差分宇宙失败"))
            return True
        # end
    
    def SelectUniverse(self):

        # 传送
        instanceNameCrop = (686.0 / 1920, 287.0 / 1080, 980.0 / 1920, 650.0 / 1080)
        instanceTypeCrop = (262.0 / 1920, 289.0 / 1080, 422.0 / 1920, 624.0 / 1080)
        screenClientMgr.ClickElement("差分宇宙", "text", crop=instanceTypeCrop)
        Flag = False

        if screenClientMgr.ClickElement("前往参与", "text", crop=instanceNameCrop):
            if "差分宇宙" in screenClientMgr.GetSingleLineText(crop=instanceNameCrop):
                screenClientMgr.PressKey("f")
            # if screenClientMgr.FindElement("「差分宇宙」", "text", crop=instanceNameCrop, takeScreenshot=True):
            #     screenClientMgr.PressKey("f")
            if screenClientMgr.ClickElement("开始游戏", "text", crop=(1466.0 / 1920, 924.0 / 1080, 246.0 / 1920, 80.0 / 1080)):
                if screenClientMgr.ClickElement("常规演算", "text", crop=(360.0 / 1920, 293.0 / 1080, 333.0 / 1920, 58.0 / 1080)):
                    Flag = True
            
        if not Flag:
            log.error(logMgr.Error("⚠️刷差分宇宙未完成 - 没有找到入口⚠️"))
            return True
        
        # 选择难度,0不是难度
        d = configMgr.mConfig[configMgr.mKey.UNIVERSE_DIFFICULTY][dataClientMgr.currentUid]
        if not d in [1,2,3,4,5]:
            log.warning(logMgr.Warning("难度设置不合法,进行难度5"))
            d = 5
        
        # 用嵌套函数
        self.SelectUniverseDifficulty(d)

        BaseClientState.DownloadChar("divergent")
        
    def SelectUniverseDifficulty(self, d):
        difficultyCrop=(85.0 / 1920, 108.0 / 1080, 94.0 / 1920, 836.0 / 1080)
        if d==0:
            log.error(logMgr.Error(f"难度{d}不合法"))
            return

        if not screenClientMgr.ClickElement(f"./assets/static/images/universe/on_{d}.png","image", 0.9, crop=difficultyCrop):
                log.info(logMgr.Info(f"未选中难度{d},尝试选择难度{d}"))
                if screenClientMgr.ClickElement(f"./assets/static/images/universe/off_{d}.png","image", 0.9, crop=difficultyCrop):
                    log.info(logMgr.Info(f"检查是否选中难度{d}"))
                    # 此处尝试无识别直接点击难度位置
                    # screenMgr.ClickElement_with_pos(((135, 160+(d-1)*110),(135, 160+(d-1)*110)))
                    if screenClientMgr.ClickElement(f"./assets/static/images/universe/on_{d}.png","image", 0.9, crop=difficultyCrop):
                        if screenClientMgr.FindElement("./assets/static/images/screen/universe/download_char.png", "image", 0.9):
                            log.info(logMgr.Info(f"已选中难度{d}"))
                            return
                        else:
                            log.warning(logMgr.Warning(f"已选中难度{d},但该难度未解锁,嵌套进入难度{d-1}"))
                            self.SelectUniverseDifficulty(d-1)
                            return
                    else:
                        log.warning(logMgr.Warning(f"可能该难度未开放,嵌套进入难度{d-1}"))
                        self.SelectUniverseDifficulty(d-1)
                        return
                else:
                    log.warning(logMgr.Warning(f"可能该难度未开放,嵌套进入难度{d-1}"))
                    self.SelectUniverseDifficulty(d-1)
                    return
        else:
            log.info(logMgr.Info(f"已选中难度{d}"))
            return
    