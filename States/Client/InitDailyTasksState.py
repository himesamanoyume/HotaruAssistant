from States.Client import *
import time
from .BaseFightState import BaseFightState

class InitDailyTasksState(BaseFightState, BaseClientState):

    mStateName = 'InitDailyTasksState'

    def OnBegin(self):
        if len(configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid]) > 0:
            dataClientMgr.dailyTasksFunctions = {
                "使用1次「万能合成机」": lambda: InitDailyTasksState.UseASynthesizer(),
                "累计触发弱点击破效果5次": lambda: InitDailyTasksState.HimekoTryWeakness5Times(),
                "累计消灭20个敌人": lambda: InitDailyTasksState.HimekoTryBeat20Enemies()
            }
        else:
            log.warning(logMgr.Warning("跳过每日任务流程"))
            return True

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    @staticmethod
    def UseASynthesizer():
        try:
            log.hr(logMgr.Hr("准备合成材料"), 2)
            screenClientMgr.ChangeTo('material')
            # 筛选规则
            if screenClientMgr.ClickElement("./assets/images/synthesis/filter.png", "image", 0.9, maxRetries=10):
                # 等待筛选界面弹出
                time.sleep(1)
                if screenClientMgr.ClickElement("通用培养材料", "text", maxRetries=3, crop=(480 / 1920, 400 / 1080, 963 / 1920, 136 / 1080)):
                    time.sleep(1)
                    if screenClientMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=10):
                        time.sleep(1)
                        # 多次重试避免选中没反应
                        for i in range(3):
                            screenClientMgr.ClickElement("./assets/images/synthesis/nuclear.png", "image", 0.9, maxRetries=3)
                            if screenClientMgr.FindElement("./assets/images/synthesis/nuclear_selected.png", "image", 0.6, maxRetries=3, crop=(1137.0 / 1920, 327.0 / 1080, 98.0 / 1920, 83.0 / 1080)):
                                if screenClientMgr.ClickElement("./assets/images/synthesis/synthesis_button.png", "image", 0.9, maxRetries=3):
                                    if screenClientMgr.ClickElement("./assets/images/base/confirm.png", "image", 0.9, maxRetries=3):
                                        if screenClientMgr.ClickElement("./assets/images/base/click_close.png", "image", 0.9, maxRetries=3):
                                            log.info(logMgr.Info("合成材料完成"))
                                            return True
                                break
            log.error(logMgr.Error("合成材料失败"))
        except Exception as e:
            log.error(logMgr.Error(f"合成材料失败: {e}"))
        return False
    
    @staticmethod
    def HimekoTryWeakness5Times():
        return True if dataClientMgr.currentHimekoTimes >= 1 else InitDailyTasksState.HimekoTry()
    
    @staticmethod
    def HimekoTryBeat20Enemies():
        if not configMgr.mConfig[configMgr.mKey.DAILY_TASKS][dataClientMgr.currentUid]['累计消灭20个敌人']:
            log.info(logMgr.Info("【累计消灭20个敌人】已被顺带完成,跳过"))
            return True
        return True if dataClientMgr.currentHimekoTimes >= 2 else ( InitDailyTasksState.HimekoTry() if dataClientMgr.currentHimekoTimes >= 1 else InitDailyTasksState.HimekoTry() and InitDailyTasksState.HimekoTry()) 


    @staticmethod
    def HimekoTry():
        screenClientMgr.ChangeTo("himeko_prepare")
        log.info(logMgr.Info("开始进行姬子试用"))
        screenClientMgr.PressKey("w", 6)
        screenClientMgr.PressMouse()
        time.sleep(1)
        screenClientMgr.PressKey("d", 2)
        screenClientMgr.PressKey("s", 2)
        screenClientMgr.PressMouse()
        time.sleep(1)
        screenClientMgr.PressKey("w", 0.5)
        screenClientMgr.PressKey("d", 2)
        screenClientMgr.PressMouse()
        time.sleep(1)
        screenClientMgr.PressKey("w", 2)
        screenClientMgr.PressMouse()
        time.sleep(3)

        # Retry.Re(lambda: screenMgr.ClickElement("./assets/images/himeko/close.png", "image", 0.9,maxRetries=1), 30)

        for i in range(10):
            if screenClientMgr.ClickElement("./assets/images/himeko/close.png", "image", 0.9, maxRetries=3):
                break
            else:    
                time.sleep(1)
        
        # bug #
        # Retry.ReThread(lambda: InitDailyTasksState.HimekoWaitFight, 240, 1)
                
        if screenClientMgr.FindElement("./assets/images/base/2x_speed_on.png", "image", 0.9, crop=(16180 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
            pass
        else:
            log.info(logMgr.Info("尝试开启二倍速"))
            screenClientMgr.PressKey("b")
            time.sleep(0.5)
            if screenClientMgr.FindElement("./assets/images/fight/fight_again.png", "image", 0.9) or screenClientMgr.FindElement("./assets/images/fight/fight_fail.png", "image", 0.9):
                log.info(logMgr.Info("检测到战斗失败/重试"))
                return False
        # end #

        time.sleep(1)
        screenClientMgr.PressKey("a")
        screenClientMgr.PressKey("a")
        screenClientMgr.PressKey("a")

        for i in range(20):
            screenClientMgr.PressKey("a")
            screenClientMgr.PressKey("a")
            screenClientMgr.PressKey("a")
            if screenClientMgr.ClickElement("./assets/images/himeko/himeko_q.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("姬子已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/herta_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选黑塔已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/natasha_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选娜塔莎已使用普攻"))
                break

        time.sleep(3)
        screenClientMgr.PressKey("d")
        time.sleep(0.5)
        for i in range(20):
            if screenClientMgr.ClickElement("./assets/images/himeko/herta_q.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("黑塔已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/himeko_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选姬子已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/natasha_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选娜塔莎已使用普攻"))
                break

        time.sleep(3)
        screenClientMgr.PressKey("a")
        screenClientMgr.PressKey("a")
        screenClientMgr.PressKey("a")
        for i in range(20):
            screenClientMgr.PressKey("a")
            screenClientMgr.PressKey("a")
            screenClientMgr.PressKey("a")
            if screenClientMgr.ClickElement("./assets/images/himeko/natasha_q.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("娜塔莎已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/himeko_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选姬子已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/herta_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选黑塔已使用普攻"))
                break

        time.sleep(10)
        for i in range(20):
            if screenClientMgr.ClickElement("./assets/images/himeko/himeko_q.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("姬子已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/herta_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选黑塔已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/natasha_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选娜塔莎已使用普攻"))
                break

        time.sleep(2)
        for i in range(20):
            if screenClientMgr.ClickElement("./assets/images/himeko/herta_q.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("黑塔已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/himeko_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选姬子已使用普攻"))
                break
            elif screenClientMgr.ClickElement("./assets/images/himeko/natasha_q.png", "image", 0.9, maxRetries=2):
                log.info(logMgr.Info("备选娜塔莎已使用普攻"))
                break
        
        time.sleep(2)
        for i in range(20):
            if screenClientMgr.ClickElement("./assets/images/himeko/natasha_e.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("娜塔莎已激活战技"))
                break
            else:
                log.info(logMgr.Info("流程出现差错,重试"))
                return InitDailyTasksState.HimekoTry()

        time.sleep(2)
        for i in range(20):
            if screenClientMgr.ClickElement("./assets/images/himeko/natasha_active_q.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("娜塔莎已释放战技"))
                break
            else:
                log.info(logMgr.Info("流程出现差错,重试"))
                return InitDailyTasksState.HimekoTry()

        time.sleep(2)
        for i in range(20):
            if screenClientMgr.FindElement("./assets/images/himeko/himeko_skill.png", "image", 0.4, maxRetries=10, crop=(229.0 / 1920, 819.0 / 1080, 109.0 / 1920, 113.0 / 1080)):
                if screenClientMgr.ClickElement("./assets/images/himeko/himeko_skill.png", "image", 0.4, maxRetries=5, crop=(229.0 / 1920, 819.0 / 1080, 109.0 / 1920, 113.0 / 1080)):
                    log.info(logMgr.Info("姬子已开启终结技"))
                    break
            else:
                log.info(logMgr.Info("流程出现差错,重试"))
                return InitDailyTasksState.HimekoTry()

        time.sleep(3)
        for i in range(20):
            if screenClientMgr.ClickElement("./assets/images/himeko/himeko_space.png", "image", 0.9, maxRetries=5):
                log.info(logMgr.Info("姬子已施放终结技"))
                break
            else:
                log.info(logMgr.Info("流程出现差错,重试"))
                return InitDailyTasksState.HimekoTry()

        time.sleep(10)
        screenClientMgr.ChangeTo("himeko_try")
        
        dataClientMgr.currentHimekoTimes += 1
        return True
        
    @staticmethod
    def HimekoWaitFight():
        if screenClientMgr.FindElement("./assets/images/base/2x_speed_on.png", "image", 0.9, crop=(1618.0 / 1920, 49.0 / 1080, 89.0 / 1920, 26.0 / 1080)):
            pass
        else:
            log.info(logMgr.Info("尝试开启二倍速"))
            screenClientMgr.PressKey("b")
            time.sleep(0.5)
            if screenClientMgr.FindElement("./assets/images/fight/fight_again.png", "image", 0.9) or screenClientMgr.FindElement("./assets/images/fight/fight_fail.png", "image", 0.9):
                log.info(logMgr.Info("检测到战斗失败/重试"))
                return
    