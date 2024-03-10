
from ruamel.yaml import YAML
from . import *
# from Hotaru.Server.LogServerHotaru import logServerMgr
from .BaseConfigModule import BaseConfigModule
from Modules.Utils.ConfigKey import ConfigKey
import time

class ConfigModule(BaseConfigModule):

    mInstance = None
    mLastTimeModifyTimestamp = 0
    mLastTimeSaveTimestamp = 0

    def __new__(cls, logMgr):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.logMgr = logMgr
            cls.mInstance.mYaml = YAML()
            cls.mInstance.mConfig = cls.mInstance.DefaultConfig("./assets/config/config.example.yaml")
            cls.mInstance.mConfigPath = "./config.yaml"
            cls.mInstance.LoadConfig()
            cls.mLastTimeSaveTimestamp = cls.mInstance.mConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP]
            
        return cls.mInstance
    
    def LoadConfig(self, configPath=None):
        configPath = self.mConfigPath if configPath is None else configPath
        try:
            with open(configPath, 'r', encoding='utf-8') as file:
                loadedConfig = self.mYaml.load(file)
                if loadedConfig:
                    self.DetectGamePath(loadedConfig)
                    self.mConfig.update(loadedConfig)
                    self.SaveConfig()
                self.logMgr.Info("Config文件已加载")
        except FileNotFoundError:
            self.logMgr.Error("Config文件未找到")
            self.SaveConfig()
        except Exception as e:
            self.logMgr.Error(f"Error loading YAML config from {configPath}: {e}")

    def SaveConfig(self):
        with open(self.mConfigPath, 'w', encoding='utf-8') as file:
            nowtime = time.time()
            self.mLastTimeSaveTimestamp = nowtime
            self.mConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP] = nowtime
            self.mYaml.dump(self.mConfig, file)

    def ReloadConfig(self):
        self.LoadConfig("./config.yaml")

    def SetValue(self, key, value):
        if key in self.mConfig:
            tempConfig = self.DefaultConfig("./assets/config/config.example.yaml")
            if tempConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP] > self.mConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP]:
                self.mConfig = tempConfig

            nowTime = time.time()
            if nowTime - self.mLastTimeModifyTimestamp >= 5:
                self.LoadConfig("./config.yaml")
                self.mLastTimeModifyTimestamp = nowTime
            self.mConfig[key] = value
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    
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

    
    def DetectKeyIsExist(self, key, uid=None, defaultValue=0):
        try:
            if uid is None:
                if self.mConfig[key] == {} or self.mConfig[key] == None:
                    self.mConfig[key] = defaultValue
            else:
                if self.mConfig[key] == {} or uid not in self.mConfig[key].keys():
                    self.mConfig[key][uid] = defaultValue
                elif self.mConfig[key][uid] == None:
                    self.mConfig[key][uid] = defaultValue
        except Exception as e:
            self.logMgr.Error(e)

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
                        
    def __getitem__(self, attr):
        if attr in self.mConfig:
            # self.logMgr.Info(f"获取值2:{attr}")
            tempConfig = self.DefaultConfig("./assets/config/config.example.yaml")
            if tempConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP] > self.mConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP]:
                self.mConfig = tempConfig

            nowTime = time.time()
            if nowTime - self.mLastTimeModifyTimestamp >= 5:
                self.LoadConfig("./config.yaml")
                self.mLastTimeModifyTimestamp = nowTime
            return self.mConfig[attr]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")
                        
    def __getattr__(self, attr):
        if attr in self.mConfig:
            tempConfig = self.DefaultConfig("./assets/config/config.example.yaml")
            if tempConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP] > self.mConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP]:
                self.mConfig = tempConfig

            nowTime = time.time()
            if nowTime - self.mLastTimeModifyTimestamp >= 5:
                self.LoadConfig("./config.yaml")
                self.mLastTimeModifyTimestamp = nowTime
            return self.mConfig[attr]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")
    
    
