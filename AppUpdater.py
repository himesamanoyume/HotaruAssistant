from Modules.Utils.Update import Update
from Modules.Config.ConfigModule import ConfigModule
from Modules.Utils.ConfigKey import ConfigKey
import sys,datetime,questionary,subprocess,os,shutil
from Modules.Utils.TitleFormatter import TitleFormatter
from Modules.Utils.FastestMirror import FastestMirror

class AppUpdater:
    mInstance = None
    
    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.logMgr = LoggerUpdateModule()
            cls.mUpdate = Update(cls.logMgr)
            cls.mConfig = ConfigModule(cls.logMgr)

        return cls.mInstance
    
    def Run(self, checkPreReleaseUpdate):
        input("按回车开始检测更新...")
        self.logMgr.Info("开始检测更新")
        try:
            isLatestTxt, isNeedUpdate, isAssetsUpdate, latestHotaruDownloadUrl, latestHotaruAssetsDownloadUrl = self.mUpdate.CheckVersion(checkPreReleaseUpdate)
            if isNeedUpdate:
                title = "发现更新:"
                optionsReg = dict()
                optionsReg.update({f"0:{isLatestTxt},执行更新":0})
                optionsReg.update({"1:不更新并退出程序":1})
                option = questionary.select(title, list(optionsReg.keys())).ask()
                value = optionsReg.get(option)
                if value == 0:
                    if isAssetsUpdate:
                        url = FastestMirror.GetGithubMirror(latestHotaruAssetsDownloadUrl)
                        self.mUpdate.InitUpdateHandler(url, os.path.abspath("./assets"), "./assets")
                    else:
                        url = FastestMirror.GetGithubMirror(latestHotaruDownloadUrl)
                        self.mUpdate.InitUpdateHandler(url, os.path.abspath("./"), "./HotaruAssistant")
                    self.mUpdate.Run()
                    input("按回车退出程序...")
                    sys.exit(0)
                elif value == 1:
                    sys.exit(0)
            else:
                self.logMgr.Warning(isLatestTxt)
                input("按回车退出程序...")
                sys.exit(0)
        except Exception as e:
            self.logMgr.Error(f"发生异常: {e}")
            input("按回车退出程序...")
            sys.exit(0)


class LoggerUpdateModule:

    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def Info(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[92mINFO\033[0m|{msg}")

    def Warning(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[93mWARNING\033[0m|\033[93m{msg}\033[0m")

    def Error(self, msg):
        currentTime = datetime.datetime.now()
        print(f"[{currentTime.hour:02d}:{currentTime.minute:02d}:{currentTime.second:02d}]\033[91mERROR\033[0m|\033[91m{msg}\033[0m")

    def Hr(self, msg, level=0):
        TitleFormatter.FormatTitle(msg, level)

if __name__ == "__main__":
    """检查临时目录并运行更新程序。"""
    if not getattr(sys, 'frozen', False):
        print("更新程序只支持打包成exe后运行")
        sys.exit(1)

    tempPath = os.path.abspath("./temp")
    filePath = sys.argv[0]
    destinationPath = os.path.join(tempPath, os.path.basename(filePath))

    try:
        if filePath != destinationPath:
            if os.path.exists(tempPath):
                shutil.rmtree(tempPath)
            if os.path.exists("./temp/Hotaru Assistant Updater.exe"):
                os.remove("./temp/Hotaru Assistant Updater.exe")
            os.makedirs(tempPath, exist_ok=True)
            shutil.copy(filePath, destinationPath)
            args = [destinationPath] + sys.argv[1:]
            subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS)
            sys.exit(0)
    except Exception as e:
        print(f"发生异常:{e}")
        input("按回车关闭窗口")
        sys.exit(0)

    appUpdater = AppUpdater()
    if sys.argv[1:] == []:
        appUpdater.Run(appUpdater.mConfig[ConfigKey.CHECK_PRERELEASE_UPDATE])
    else:
        appUpdater.Run(sys.argv[1:])