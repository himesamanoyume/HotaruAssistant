
from ruamel.yaml import YAML
from . import *
from Modules.Utils.ConfigKey import ConfigKey
import time,threading

class ConfigModule():

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
            cls.mLastTimeSaveTimestamp = cls.mInstance.mConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP]
            
        return cls.mInstance
    
    def LoadConfig(self, configPath=None):
        configPath = self.mConfigPath if configPath is None else configPath
        try:
            with open(configPath, 'r', encoding='utf-8') as file:
                tempLoadConfig = self.mYaml.load(file)
                # 说明配置文件最后保存的时间戳比脚本中的要新,因此替换掉脚本中加载的配置文件
                if tempLoadConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP] - self.mLastTimeSaveTimestamp >= 5:
                    self.mConfig.update(tempLoadConfig)
                    self.SaveConfig()
                    self.logMgr.Debug("Config文件已重载")
        except FileNotFoundError:
            self.logMgr.Error("Config文件未找到")
            self.SaveConfig()
        except Exception as e:
            self.logMgr.Error(f"加载YAML配置文件 {configPath}出错: {e}")

    def SaveConfig(self):
        with open(self.mConfigPath, 'w', encoding='utf-8') as file:
            self.logMgr.Info("Config已保存")
            nowtime = time.time()
            self.mLastTimeSaveTimestamp = nowtime
            self.mConfig[ConfigKey.LAST_TIME_SAVE_TIMESTAMP] = nowtime
            self.mYaml.dump(self.mConfig, file)

    def ReloadConfig(self):
        self.LoadConfig("./config.yaml")

    def SetValue(self, key, value):
        if key in self.mConfig:
            self.ReloadConfig()

            nowTime = time.time()
            if nowTime - self.mLastTimeModifyTimestamp >= 5:
                self.ReloadConfig()
                self.mLastTimeModifyTimestamp = nowTime
            self.logMgr.Debug(f"config: {key}被修改")
            self.mConfig[key] = value
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
        
    def DelValue(self, key, uid:str=None):
        if key in self.mConfig:
            self.ReloadConfig()

            nowTime = time.time()
            if nowTime - self.mLastTimeModifyTimestamp >= 5:
                self.ReloadConfig()
                self.mLastTimeModifyTimestamp = nowTime

            if uid:
                del self.mConfig[key][uid]
            else:
                del self.mConfig[key]
            self.logMgr.Debug(f"config: {key}被删除")
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    
    @classmethod
    def DefaultConfig(cls, exampleConfigPath):
        try:
            with open(exampleConfigPath, 'r', encoding='utf-8') as file:
                loadedConfig = cls.mInstance.mYaml.load(file)
                if loadedConfig:
                    cls.logMgr.Debug("Config文件已首次加载")
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
            
            t = threading.Thread(target=self.SetTimestamp)
            t.start()

            self.logMgr.Debug(f"config: {attr}被获取")
            return self.mConfig[attr]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")
    
    def SetTimestamp(self):
        self.nowTime = time.time()
        if self.nowTime - self.mLastTimeModifyTimestamp >= 5:
            self.mLastTimeModifyTimestamp = self.nowTime
            self.ReloadConfig()
            self.logMgr.Debug("Config已重载")
                        
    def __getattr__(self, attr):
        if attr in self.mConfig:

            t = threading.Thread(target=self.SetTimestamp)
            t.start()

            self.logMgr.Debug(f"config: {attr}被获取")
            return self.mConfig[attr]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")
    
    
