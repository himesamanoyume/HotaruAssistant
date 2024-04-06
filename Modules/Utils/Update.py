
import urllib.request,os,subprocess,tempfile,shutil
from packaging.version import parse
from tqdm import tqdm
from Modules.Utils.FastestMirror import FastestMirror
import requests,json

class Update:
    mInstance = None

    def __new__(cls, log):
        if cls.mInstance is None:
            cls.mInstance = super().__new__(cls)
            cls.log = log
        return cls.mInstance
    
    def Run(self):
        self.DownloadFile()
        self.ExtractFile()
        self.CoverFolder()
        self.CleanUp()

    def DownloadWithProgress(self, downloadUrl, savePath):
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
                self.log.info(f"开始下载: {self.downloadUrl}")
                self.DownloadWithProgress(self.downloadUrl, self.downloadFilePath)
                self.log.info(f"下载完成: {self.downloadFilePath}")
                break
            except Exception as e:
                self.log.error(f"下载失败: {e}")
                input("可以按回车键重试,或重开程序尝试获取到其他下载链接. . .")

    def ExtractFile(self):
        while True:
            try:
                if not subprocess.run([self.exePath, "x", self.downloadFilePath, f"-o{self.tempPath}", "-aoa"], shell=True, check=True):
                    raise Exception
                self.log.info(f"解压完成：{self.extractFolderPath}")
                break
            except Exception as e:
                self.log.error(f"解压失败：{e}")
                input("按回车键重试. . .")

    def CoverFolder(self):
        while True:
            try:
                shutil.copytree(self.extractFolderPath, self.coverFolderPath, dirs_exist_ok=True)
                self.log.info(f"覆盖完成：{self.coverFolderPath}")
                break
            except Exception as e:
                self.log.error(f"覆盖失败：{e}")
                input("按回车键重试. . .")

    def CleanUp(self):
        try:
            os.remove(self.downloadFilePath)
            self.log.info(f"清理完成：{self.downloadFilePath}")
        except Exception as e:
            self.log.warning(f"清理失败：{e}")
        try:
            shutil.rmtree(self.extractFolderPath)
            self.log.info(f"清理完成：{self.extractFolderPath}")
        except Exception as e:
            self.log.warning(f"清理失败：{e}")

    @staticmethod
    def CheckVersion(isCheckPreRelease):
        try:
            with open("./assets/config/version.txt", 'r', encoding='utf-8') as txtFile:
                currentHotaruVersion = txtFile.read()
                txtFile.close()
            with open("./assets/config/meta.json", 'r', encoding='utf-8') as jsonFile:
                currentAssetsVersion = json.load(jsonFile)['hotaru_assets_version']
                jsonFile.close()

            response = requests.get(FastestMirror.GetGithubApiMirror("himesamanoyume","HotaruAssistant", 5, isCheckPreRelease), timeout=3)
            if response.status_code == 200:
                data = json.loads(response.text)
                if isCheckPreRelease:
                    for item in data:
                        if item["prerelease"]:
                            data = item
                            break

                    data = data[0]
                    
                latestHotaruVersion = data["tag_name"]
                latestHotaruDownloadUrl = None
                latestHotaruAssetsDownloadUrl = None
                for asset in data["assets"]:
                    if "HotaruAssistantAssets_" in asset["browser_download_url"]:
                        latestHotaruAssetsDownloadUrl = asset["browser_download_url"]
                        latestAssetsVersion = latestHotaruAssetsDownloadUrl.split("HotaruAssistantAssets_")[1].split(".zip")[0]
                    elif 'HotaruAssistant_' in asset["browser_download_url"]:
                        latestHotaruDownloadUrl = asset["browser_download_url"]
                            
                    if not (latestHotaruDownloadUrl is None) and not(latestHotaruAssetsDownloadUrl is None):
                        break
                # 比较本地版本
                isLatestTxt = ""
                isNeedUpdate = False
                isAssetsUpdate = False

                if parse(latestHotaruVersion.lstrip('v')) > parse(currentHotaruVersion.lstrip('v')):
                    isLatestTxt = f"发现助手新版本：{currentHotaruVersion} ——> {latestHotaruVersion}"
                    isNeedUpdate = True
                else:
                    if parse(latestAssetsVersion.lstrip('v')) > parse(currentAssetsVersion.lstrip('v')):
                        isLatestTxt = f"发现资源新版本：{currentAssetsVersion} ——> {latestAssetsVersion}"
                        isNeedUpdate = True
                        isAssetsUpdate = True
                    else:
                        isLatestTxt = f"当前助手和资源包皆已是最新版本: {currentHotaruVersion}, {currentAssetsVersion}"

                return isLatestTxt, isNeedUpdate, isAssetsUpdate, latestHotaruDownloadUrl, latestHotaruAssetsDownloadUrl
            else:
                isLatestTxt = f"检测更新失败: {response.text}"
                return isLatestTxt, False, False, None, None
        except Exception as e:
            isLatestTxt = f"检测更新异常: {e}"
            return isLatestTxt, False, False, None, None