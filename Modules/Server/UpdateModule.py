from Hotaru.Server.LogServerHotaru import logMgr
from Hotaru.Server.ConfigServerHotaru import configMgr
from Hotaru.Server.DataServerHotaru import dataMgr
import requests,json,urllib.request,os,subprocess,tempfile,shutil,sys,questionary
from packaging.version import parse
from tqdm import tqdm

class UpdateModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def Run(self):
        self.DownloadFile()
        self.ExtractFile()
        self.CoverFolder()
        self.CleanUp()
    
    def DetectVersionUpdate(self):
        logMgr.Info("开始检测更新")
        if not configMgr.mConfig[configMgr.mKey.CHECK_UPDATE]:
            logMgr.Error("检测更新未开启")
            return False

        isLatestTxt = dataMgr.isLatestTxt
        isNeedUpdate = dataMgr.isNeedUpdate

        if isNeedUpdate:
            title = "选择退出Server/不更新并继续使用:"
            optionsReg = dict()
            optionsReg.update({f"0:退出Server {isLatestTxt}":0})
            optionsReg.update({"1:不更新并继续使用":1})
            option = questionary.select(title, list(optionsReg.keys())).ask()
            value = optionsReg.get(option)
            if value == 0:
                sys.exit(0)
            elif value == 1:
                return
        else:
            logMgr.Warning(isLatestTxt)


    def DownloadWithProgress(downloadUrl, savePath):
        response = urllib.request.urlopen(downloadUrl)
        file_size = int(response.info().get('Content-Length', -1))

        # 使用 tqdm 创建进度条
        with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            def update_bar(block_count, block_size, total_size):
                if pbar.total != total_size:
                    pbar.total = total_size
                downloaded = block_count * block_size
                pbar.update(downloaded - pbar.n)

            urllib.request.urlretrieve(downloadUrl, savePath, reporthook=update_bar)

    def InitUpdateHandler(self, downloadUrl, coverFolderPath, extractFileName):
        self.exePath = os.path.abspath("./assets/7z/7za.exe")
        self.tempPath = tempfile.gettempdir()
        self.downloadUrl = downloadUrl
        self.downloadFilePath = os.path.join(self.tempPath, os.path.basename(downloadUrl))
        self.coverFolderPath = coverFolderPath
        self.extractFolderPath = os.path.join(self.tempPath, os.path.basename(extractFileName))

    def DownloadFile(self):
        while True:
            try:
                logMgr.Info(f"开始下载: {self.downloadUrl}")
                self.DownloadWithProgress(self.downloadUrl, self.downloadFilePath)
                logMgr.Info(f"下载完成: {self.downloadFilePath}")
                break
            except Exception as e:
                logMgr.Error(f"下载失败: {e}")
                input("按回车键重试. . .")

    def ExtractFile(self):
        while True:
            try:
                if not subprocess.run([self.exePath, "x", self.downloadFilePath, f"-o{self.tempPath}", "-aoa"], shell=True, check=True):
                    raise Exception
                logMgr.Info(f"解压完成：{self.extractFolderPath}")
                break
            except Exception as e:
                logMgr.Error(f"解压失败：{e}")
                input("按回车键重试. . .")

    def CoverFolder(self):
        while True:
            try:
                shutil.copytree(self.extractFolderPath, self.coverFolderPath, dirs_exist_ok=True)
                logMgr.Info(f"覆盖完成：{self.coverFolderPath}")
                break
            except Exception as e:
                logMgr.Error(f"覆盖失败：{e}")
                input("按回车键重试. . .")

    def CleanUp(self):
        try:
            os.remove(self.downloadFilePath)
            logMgr.Info(f"清理完成：{self.downloadFilePath}")
        except Exception as e:
            logMgr.Warning(f"清理失败：{e}")
        try:
            shutil.rmtree(self.extractFolderPath)
            logMgr.Info(f"清理完成：{self.extractFolderPath}")
        except Exception as e:
            logMgr.Warning(f"清理失败：{e}")