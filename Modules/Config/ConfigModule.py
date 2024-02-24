
from ruamel.yaml import YAML
import sys,questionary
from .ConfigKeySubModule import ConfigKeySubModule
from Mgrs.HotaruServerMgr import LogServerMgr

class ConfigModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mInstance.LoadConfig()
            cls.mConfigKey = ConfigKeySubModule()
        return cls.mInstance
    
    def LoadConfig(self, configPath=None, exampleConfigPath = "./Assets/config/config.example.yaml"):
        self.mConfigPath = configPath
        self.mYaml = YAML()

        try:
            with open(exampleConfigPath, 'r', encoding='utf-8') as exampleConfigFile:
                exampleConfig = self.mYaml.load(exampleConfigFile)
                if exampleConfig:
                    self.mExampleConfig = exampleConfig
                LogServerMgr.Info("Config文件已加载")
        except FileNotFoundError:
            LogServerMgr.Error("Config文件未找到")
            sys.exit(1)
        
        configPath = self.mConfigPath if configPath is None else configPath
    
    def ReadConfigByUid(self, uid):
        pass

    @classmethod
    def IsAgreeDisclaimer(cls):
        #  if not  xx[cls.mConfigKey.agreed_to_disclaimer]:
            cls.ShowDisclaimer()
        #   else
            
    
    @staticmethod
    def ShowDisclaimer():
        LogServerMgr.Hr("《免责声明》")
        LogServerMgr.Hr('本软件是一个外部工具旨在自动化崩坏星轨的游戏玩法。它被设计成仅通过现有用户界面与游戏交互,并遵守相关法律法规。该软件包旨在提供简化和用户通过功能与游戏交互,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。\nThis software is open source, free of charge and for learning and exchange purposes only. The developer team has the final right to interpret this project. All problems arising from the use of this software are not related to this project and the developer team. If you encounter a merchant using this software to practice on your behalf and charging for it, it may be the cost of equipment and time, etc. The problems and consequences arising from this software have nothing to do with it.\n本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。\n根据MiHoYo的 [崩坏:星穹铁道的公平游戏宣言]：\n"严禁使用外挂、加速器、脚本或其他破坏游戏公平性的第三方工具。"\n"一经发现，米哈游（下亦称“我们”）将视违规严重程度及违规次数，采取扣除违规收益、冻结游戏账号、永久封禁游戏账号等措施。"')
        selectTitle = '你是否接受?'
        options = dict()
        options.update({"我接受":0})
        options.update({"我拒绝":1})
        option = questionary.select(selectTitle, list(options.keys())).ask()
        value = options.get(option)
        if value == 0:
            # config.set_value("agreed_to_disclaimer", True)
            pass
        else:
            LogServerMgr.Hr("您未同意《免责声明》")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
