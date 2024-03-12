
from Modules.Utils.ConfigKey import ConfigKey
from Modules.Config.ConfigModule import ConfigModule
from Hotaru.Server.LogServerHotaru import logMgr
import sys,questionary,threading,time

class ConfigServerMgr:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mConfig = ConfigModule(logMgr)
            cls.mKey = ConfigKey()

        return cls.mInstance
    
    def AutoSave(self):
        while True:
            time.sleep(1)
            if time.time() - self.mConfig.mLastTimeModifyTimestamp <= 5:
                logMgr.Info("检测到配置文件修改")
                time.sleep(5)
                if time.time() - self.mConfig.mLastTimeModifyTimestamp >= 5:
                    self.mConfig.SaveConfig()
                    logMgr.Info("配置文件已自动保存")
    
    def IsAgreed2Disclaimer(self):
        if not self.mConfig[self.mKey.AGREED_TO_DISCLAIMER]:
            self.ShowDisclaimer()

        self.autoSaveThread = threading.Thread(target=self.AutoSave)
        self.autoSaveThread.start()
    
    def ShowDisclaimer(self):
        logMgr.Hr("《免责声明》")
        logMgr.Hr('本软件是一个外部工具旨在自动化崩坏星轨的游戏玩法。它被设计成仅通过现有用户界面与游戏交互,并遵守相关法律法规。该软件包旨在提供简化和用户通过功能与游戏交互,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。\nThis software is open source, free of charge and for learning and exchange purposes only. The developer team has the final right to interpret this project. All problems arising from the use of this software are not related to this project and the developer team. If you encounter a merchant using this software to practice on your behalf and charging for it, it may be the cost of equipment and time, etc. The problems and consequences arising from this software have nothing to do with it.\n本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。\n根据MiHoYo的 [崩坏:星穹铁道的公平游戏宣言]：\n"严禁使用外挂、加速器、脚本或其他破坏游戏公平性的第三方工具。"\n"一经发现，米哈游（下亦称“我们”）将视违规严重程度及违规次数，采取扣除违规收益、冻结游戏账号、永久封禁游戏账号等措施。"')
        logMgr.Warning("就此离开，没人会受伤。否则，你们都会死...")
        selectTitle = '你是否接受?'
        options = dict()
        options.update({"我接受":0})
        options.update({"我拒绝":1})
        option = questionary.select(selectTitle, list(options.keys())).ask()
        value = options.get(option)
        if value == 0:
            self.mConfig.SetValue(self.mKey.AGREED_TO_DISCLAIMER, True)
        else:
            logMgr.Info("您未同意《免责声明》")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
    
