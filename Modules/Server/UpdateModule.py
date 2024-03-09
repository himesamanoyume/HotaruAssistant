from Hotaru.Server.LogServerHotaru import logMgr
from Hotaru.Server.ConfigServerHotaru import configMgr
from Modules.Utils.FastestMirror import FastestMirror
import requests,json,urllib.request,os,subprocess,tempfile,shutil,sys,questionary
from packaging.version import parse
from tqdm import tqdm

class UpdateModule:
    mInstance = None

    def __new__(cls):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
        return cls.mInstance
    
    @classmethod
    def Run(cls):
        cls.DownloadFile()
        cls.ExtractFile()
        cls.CoverFolder()
        cls.CleanUp()
    
    @classmethod
    def DetectVersionUpdate(cls):
        logMgr.Info("开始检测更新")
        if not configMgr.mConfig[configMgr.mKey.CHECK_UPDATE]:
            logMgr.Error("检测更新未开启")
            return False

        try:
            with open("./assets/config/version.txt", 'r', encoding='utf-8') as txtFile:
                cls.currentHotaruVersion = txtFile.read()
                txtFile.close()
            with open("./assets/config/meta.json", 'r', encoding='utf-8') as jsonFile:
                cls.currentAssetsVersion = json.load(jsonFile)['hotaru_assets_version']
                jsonFile.close()

            response = requests.get(FastestMirror.GetGithubApiMirror("himesamanoyume","himesamanoyume","latest.json",1), timeout=3)
            if response.status_code == 200:
                data = json.loads(response.text)
                

                # —————————————————————————————暂时注释———————————————————————————————

                # cls.latestHotaruVersion = data["tag_name"]
                # for asset in data["assets"]:
                #     if "Assets" in asset["browser_download_url"]:
                #         cls.downloadAssetsUrl = asset["browser_download_url"]
                #         cls.latestAssetsVersion = cls.downloadAssetsUrl.split("HotaruAssistantAssets_")[1].split(".zip")[0]
                #         break

                # ——————————————————————————————————————————————————————————————————

                cls.latestHotaruVersion = "v2.0.1"
                cls.downloadAssetsUrl = "https://github.com/himesamanoyume/himesamanoyume/releases/download/v2.0.0/HotaruAssistantAssets_v2.0.1.b.zip"
                cls.latestAssetsVersion = cls.downloadAssetsUrl.split("HotaruAssistantAssets_")[1].split(".zip")[0]

                # ——————————————————————————————————————————————————————————————————

                # 比较本地版本
                isLatestTxt = ""
                isNeedUpdate = False

                if parse(cls.latestHotaruVersion.lstrip('v')) > parse(cls.currentHotaruVersion.lstrip('v')):
                    logMgr.Warning(f"发现助手新版本：{cls.currentHotaruVersion} ——> {cls.latestHotaruVersion}\n需要退出Server并启动Update进行更新!")
                    isLatestTxt = "[检测到助手新版本,应选择退出Server,之后请手动启动Update进行更新]"
                    isNeedUpdate = True
                else:
                    logMgr.Info(f"当前助手已是最新版本: {cls.currentAssetsVersion}, 开始检测资源版本")
                    if parse(cls.latestAssetsVersion.lstrip('v')) > parse(cls.currentAssetsVersion.lstrip('v')):
                        logMgr.Warning(f"发现资源新版本：{cls.currentAssetsVersion} ——> {cls.latestAssetsVersion}\n需要退出Server并启动Update进行更新!")
                        isLatestTxt = "[检测到资源新版本,应选择退出Server,之后请手动启动Update进行更新]"
                        isNeedUpdate = True
                    else:
                        logMgr.Info(f"当前已是最新版本: {cls.currentAssetsVersion}")

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
                logMgr.Error("检测更新失败")
                logMgr.Error(response.text)
        except Exception as e:
            logMgr.Error(f"检测更新失败:{e}")
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
                logMgr.Info(f"开始下载: {cls.downloadUrl}")
                cls.DownloadWithProgress(cls.downloadUrl, cls.downloadFilePath)
                logMgr.Info(f"下载完成: {cls.downloadFilePath}")
                break
            except Exception as e:
                logMgr.Error(f"下载失败: {e}")
                input("按回车键重试. . .")

    @classmethod
    def ExtractFile(cls):
        while True:
            try:
                if not subprocess.run([cls.exePath, "x", cls.downloadFilePath, f"-o{cls.tempPath}", "-aoa"], shell=True, check=True):
                    raise Exception
                logMgr.Info(f"解压完成：{cls.extractFolderPath}")
                break
            except Exception as e:
                logMgr.Error(f"解压失败：{e}")
                input("按回车键重试. . .")

    @classmethod
    def CoverFolder(cls):
        while True:
            try:
                shutil.copytree(cls.extractFolderPath, cls.coverFolderPath, dirs_exist_ok=True)
                logMgr.Info(f"覆盖完成：{cls.coverFolderPath}")
                break
            except Exception as e:
                logMgr.Error(f"覆盖失败：{e}")
                input("按回车键重试. . .")

    @classmethod
    def CleanUp(cls):
        try:
            os.remove(cls.downloadFilePath)
            logMgr.Info(f"清理完成：{cls.downloadFilePath}")
        except Exception as e:
            logMgr.Warning(f"清理失败：{e}")
        try:
            shutil.rmtree(cls.extractFolderPath)
            logMgr.Info(f"清理完成：{cls.extractFolderPath}")
        except Exception as e:
            logMgr.Warning(f"清理失败：{e}")