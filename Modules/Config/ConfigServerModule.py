
from ruamel.yaml import YAML
import sys,questionary,os
from pylnk3 import Lnk
from .ConfigKeySubModule import ConfigKeySubModule
from Hotaru.Server.LogServerHotaru import logServerMgr
from Modules.Config.BaseConfigModule import BaseConfigModule

class ConfigServerModule(BaseConfigModule):

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.mInstance.mYaml = YAML()
            cls.mInstance.mConfig = cls.mInstance.DefaultConfig("./assets/config/config.example.yaml")
            cls.mInstance.mConfigPath = "./config.yaml"
            cls.mInstance.LoadConfig()
        return cls.mInstance
    
    @classmethod
    def IsAgreeDisclaimer(cls):
        #  if not  xx[cls.mConfigKey.agreed_to_disclaimer]:
        if not cls.GetConfigValue(cls.mConfigKey.common.agreed_to_disclaimer):
            cls.ShowDisclaimer()

    
    def LoadConfig(self, configPath=None):
        configPath = self.mConfigPath if configPath is None else configPath
        try:
            with open(configPath, 'r', encoding='utf-8') as file:
                loadedConfig = self.mYaml.load(file)
                if loadedConfig:
                    self.DetectGamePath(loadedConfig)
                    self.mConfig.update(loadedConfig)
                    self.SaveConfig()
                print("Config文件已加载")
        except FileNotFoundError:
            print("Config文件未找到")
            self.SaveConfig()
        except Exception as e:
            print(f"Error loading YAML config from {configPath}: {e}")

    @classmethod
    def SaveConfig(cls):
        with open(cls.mInstance.mConfigPath, 'w', encoding='utf-8') as file:
            cls.mInstance.mYaml.dump(cls.mInstance.mConfig, file)
    
    @classmethod
    def DefaultConfig(cls, exampleConfigPath):
        try:
            with open(exampleConfigPath, 'r', encoding='utf-8') as file:
                loadedConfig = cls.mInstance.mYaml.load(file)
                if loadedConfig:
                    # print("初始配置文件已加载")
                    return loadedConfig
        except FileNotFoundError:
            input("初始配置文件未找到,检查assets是否完整")
            sys.exit(1)

    @classmethod
    def GetConfigValue(cls, key:str, uid:str=None):
        try:
            if uid is None:
                return cls.mInstance.mConfig[key]
            else:
                return cls.mInstance.mConfig[key][uid]
        except Exception as e:
            print(e)

    @classmethod
    def SetConfigValue(cls, key:str, uid:str=None, value=0):
        try:
            if uid is None:
                cls.mInstance.mConfig[key] = value
            else:
                cls.mInstance.mConfig[key][uid] = value
            cls.SaveConfig()
        except Exception as e:
            print(e)

    def DetectGamePath(self, config):
        game_path = config['game_path']
        if os.path.exists(game_path):
            return
        start_menu_path = os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs", "崩坏：星穹铁道")
        try:
            with open(os.path.join(start_menu_path, "崩坏：星穹铁道.lnk"), "rb") as lnk_file:
                lnk = Lnk(lnk_file)
                program_config_path = os.path.join(lnk.work_dir, "config.ini")
        except:
            program_config_path = os.path.join(os.getenv('ProgramFiles'), "Star Rail\\config.ini")
        if os.path.exists(program_config_path):
            with open(program_config_path, 'r', encoding='utf-8') as file:
                for line in file.readlines():
                    if line.startswith("game_install_path="):
                        game_path = line.split('=')[1].strip()
                        if os.path.exists(game_path):
                            config['game_path'] = os.path.join(game_path, "StarRail.exe")
                            return
                        
    def __getattr__(self, attr):
        if attr in self.mConfig:
            return self.mConfig[attr]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")
    
    @classmethod
    def ShowDisclaimer(cls):
        logServerMgr.Info("《免责声明》")
        logServerMgr.Info('本软件是一个外部工具旨在自动化崩坏星轨的游戏玩法。它被设计成仅通过现有用户界面与游戏交互,并遵守相关法律法规。该软件包旨在提供简化和用户通过功能与游戏交互,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。\nThis software is open source, free of charge and for learning and exchange purposes only. The developer team has the final right to interpret this project. All problems arising from the use of this software are not related to this project and the developer team. If you encounter a merchant using this software to practice on your behalf and charging for it, it may be the cost of equipment and time, etc. The problems and consequences arising from this software have nothing to do with it.\n本软件开源、免费，仅供学习交流使用。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。\n根据MiHoYo的 [崩坏:星穹铁道的公平游戏宣言]：\n"严禁使用外挂、加速器、脚本或其他破坏游戏公平性的第三方工具。"\n"一经发现，米哈游（下亦称“我们”）将视违规严重程度及违规次数，采取扣除违规收益、冻结游戏账号、永久封禁游戏账号等措施。"')
        selectTitle = '你是否接受?'
        options = dict()
        options.update({"我接受":0})
        options.update({"我拒绝":1})
        option = questionary.select(selectTitle, list(options.keys())).ask()
        value = options.get(option)
        if value == 0:
            # logServerMgr.Info(cls.GetConfigValue(cls.mConfigKey.common.agreed_to_disclaimer))
            cls.SetConfigValue(cls.mConfigKey.common.agreed_to_disclaimer, value=True)
        else:
            logServerMgr.Info("您未同意《免责声明》")
            input("按回车键关闭窗口. . .")
            sys.exit(0)
