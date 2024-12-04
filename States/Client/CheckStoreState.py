from States.Client import *
from Hotaru.Client.ConfigClientHotaru import configMgr
from Hotaru.Client.DataClientHotaru import dataClientMgr
from Modules.Utils.Date import Date

class CheckStoreState(BaseClientState):

    mStateName = 'CheckStoreState'

    def OnBegin(self):
        self.ExpressSupplyPass()
        if configMgr.mConfig[configMgr.mKey.STORE_ENABLE][dataClientMgr.currentUid]:
            self.EmbersExchange()

    def OnRunning(self):
        return False

    def OnExit(self):
        return False
    
    def ExpressSupplyPass(self):
        screenClientMgr.ChangeTo('menu')
        if screenClientMgr.ClickElement("./assets/static/images/menu/store.png", "image", 0.9):
            temp = screenClientMgr.GetSingleLineText(crop=(511.0 / 1920, 885.0 / 1080, 398.0 / 1920, 51.0 / 1080))
            if not temp == None:
                remainingText = temp.split('：')[1]
                dataClientMgr.passRemaining = remainingText
            else:
                log.info(logMgr.Info("没有购买月卡"))
        else:
            log.warning(logMgr.Warning("无法检测月卡剩余天数"))
            return True
        
    def EmbersExchange(self):
        def DetectEmbers():
            embers = screenClientMgr.GetSingleLineText(crop=(1672.0 / 1920, 43.0 / 1080, 99.0 / 1920, 45.0 / 1080))
            log.info(logMgr.Info(f"当前剩余余烬:{embers}"))
            return int(embers)
        
        def DetectRemainCount(product):
            remainCountText = screenClientMgr.GetSingleLineText(crop=(513.0 / 1920, 613.0 / 1080, 120.0 / 1920, 41.0 / 1080))
            remainCount = int(remainCountText.replace(' ', '').split('可兑换')[1].split('/')[0])
            log.info(logMgr.Info(f"当前{product}剩余数量:{remainCount}"))
            return remainCount
        
        def GetMaxCount(embers, productPrice, remainCount):
            maxCount = embers // productPrice
            maxCount = min(maxCount, remainCount)
            log.info(logMgr.Info(f"当前可兑换的最大数量:{maxCount}"))
            return maxCount


        if screenClientMgr.ClickElement("余烬兑换", "text", 0.9, crop=(104.0 / 1920, 358.0 / 1080, 122.0 / 1920, 46.0 / 1080)):
            price = {"星轨专票":90, "星轨通票":90, "命运的足迹":60}
            for product in configMgr.mConfig[configMgr.mKey.STORE_PRODUCT_PRIORITY][dataClientMgr.currentUid]:
                if not Date.IsNextMonth4AM(configMgr.mConfig[configMgr.mKey.STORE_SOLDOUT_TIMESTAMP][product][dataClientMgr.currentUid]):
                    log.debug(logMgr.Debug(f"由于{product}已售罄,将其移除出购买清单"))
                    price.pop(product)
            
            if not len(price.keys()) > 0:
                log.info(logMgr.Info(f"当前已兑换完所有超值商品"))
            else:
                for product in configMgr.mConfig[configMgr.mKey.STORE_PRODUCT_PRIORITY][dataClientMgr.currentUid]:
                    if not product in price.keys() or not configMgr.mConfig[configMgr.mKey.STORE_PRODUCT_ENABLE][product][dataClientMgr.currentUid]:
                        continue

                    if screenClientMgr.ClickElement(product, "text", 0.9, crop=(379.0 / 1920, 305.0 / 1080, 603.0 / 1920, 36.0 / 1080)):
                        embers = DetectEmbers()
                        remainCount = DetectRemainCount(product)
                        maxCount = GetMaxCount(embers, price[product], remainCount)
                        for i in range(maxCount-1):
                            screenClientMgr.ClickElement("./assets/static/images/share/trailblaze_power/plus.png", "image", 0.9)

                        if screenClientMgr.ClickElement("./assets/static/images/base/confirm.png", "image", 0.9):
                            screenClientMgr.ClickElement("点击空白处关闭", "text", 0.8)
                            if remainCount == maxCount:
                                log.info(logMgr.Info(f"已兑换完所有{product}"))
                                configMgr.mConfig[configMgr.mKey.STORE_SOLDOUT_TIMESTAMP][product][dataClientMgr.currentUid] = time.time()
                    else:
                        log.info(logMgr.Info(f"未找到{product}"))
                                
                    
