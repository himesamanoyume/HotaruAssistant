from Hotaru.Server.LogServerHotaru import logServerMgr
from Hotaru.Server.ConfigServerHotaru import configServerMgr
from Modules.Utils.FastestMirror import FastestMirror
import requests,json,urllib.request,os,subprocess,tempfile,shutil
from packaging.version import parse
from tqdm import tqdm

class UpdateModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    def DetectVersionUpdate():
        if not configServerMgr.GetConfigValue(configServerMgr.mConfig.mCommonKey.check_update):
            logServerMgr.Error("检测更新未开启")
            return False
        logServerMgr.Info("开始检测更新")
        try:
            response = requests.get(FastestMirror.GetGithubApiMirror("himesamanoyume","HotaruAssistant","latest.json",1), timeout=3)
            if response.status_code == 200:
                data = json.loads(response.text)
                version:str = data["tag_name"]
                logServerMgr.Info(f"最新版本:{version},当前版本:{configServerMgr.GetConfigValue(configServerMgr.mConfig.mCommonKey.hotaru_version)}")
                if parse(version.lstrip('v')) > parse(configServerMgr.mConfig.mCommonKey.hotaru_version.lstrip('v')):
                    logServerMgr.Warning(f"发现新版本!需要退出Server和Client后启动Update进行更新!")
                    logServerMgr.Info(data["html_url"])
                else:
                    logServerMgr.Info("已经是最新版本")
            else:
                logServerMgr.Error("检测更新失败")
                # logger.debug(response.text)
        except Exception as e:
            logServerMgr.Error(f"检测更新失败:{e}")
            # logger.debug(e)


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

    @classmethod
    def InitUpdateHandler(cls, downloadUrl, coverFolderPath, extractFileName):
        cls.exePath = os.path.abspath("./assets/7z/7za.exe")
        cls.tempPath = tempfile.gettempdir()
        cls.downloadUrl = downloadUrl
        cls.downloadFilePath = os.path.join(cls.tempPath, os.path.basename(downloadUrl))
        cls.coverFolderPath = coverFolderPath
        cls.extractFolderPath = os.path.join(cls.tempPath, os.path.basename(extractFileName))

    @classmethod
    def DownloadFile(cls):
        while True:
            try:
                logServerMgr.Info(f"开始下载: {cls.downloadUrl}")
                cls.DownloadWithProgress(cls.downloadUrl, cls.downloadFilePath)
                logServerMgr.Info(f"下载完成: {cls.downloadFilePath}")
                break
            except Exception as e:
                logServerMgr.Error(f"下载失败: {e}")
                input("按回车键重试. . .")

    @classmethod
    def ExtractFile(cls):
        while True:
            try:
                if not subprocess.run([cls.exePath, "x", cls.downloadFilePath, f"-o{cls.tempPath}", "-aoa"], shell=True, check=True):
                    raise Exception
                logServerMgr.Info(f"解压完成：{cls.extractFolderPath}")
                break
            except Exception as e:
                logServerMgr.Error(f"解压失败：{e}")
                input("按回车键重试. . .")

    @classmethod
    def CoverFolder(cls):
        while True:
            try:
                shutil.copytree(cls.extractFolderPath, cls.coverFolderPath, dirs_exist_ok=True)
                logServerMgr.Info(f"覆盖完成：{cls.coverFolderPath}")
                break
            except Exception as e:
                logServerMgr.Error(f"覆盖失败：{e}")
                input("按回车键重试. . .")

    @classmethod
    def CleanUp(cls):
        try:
            os.remove(cls.downloadFilePath)
            logServerMgr.Info(f"清理完成：{cls.downloadFilePath}")
        except Exception as e:
            logServerMgr.Warning(f"清理失败：{e}")
        try:
            shutil.rmtree(cls.extractFolderPath)
            logServerMgr.Info(f"清理完成：{cls.extractFolderPath}")
        except Exception as e:
            logServerMgr.Warning(f"清理失败：{e}")