
import urllib.request,os,subprocess,tempfile,shutil,questionary
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
    
    def Run(self, isAssetsUpdate = False):
        self.DownloadFile()
        self.ExtractFile()
        self.CoverFolder(isAssetsUpdate)
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

    def InitUpdateHandler(self, originalDownloadUrl, downloadUrl, coverFolderPath, extractFileName):
        self.exePath = os.path.abspath("./assets/7z/7za.exe")
        self.tempPath = tempfile.gettempdir()
        self.originalDownloadUrl = originalDownloadUrl
        self.downloadUrl = downloadUrl
        self.downloadFilePath = os.path.join(self.tempPath, os.path.basename(downloadUrl))
        self.coverFolderPath = coverFolderPath
        self.extractFolderPath = os.path.join(self.tempPath, os.path.basename(extractFileName))

    def DownloadFile(self):
        value = 0
        while True:
            try:
                if value == 0:
                    self.log.info(f"开始下载: {self.downloadUrl}")
                    self.DownloadWithProgress(self.downloadUrl, self.downloadFilePath)
                    self.log.info(f"下载完成: {self.downloadFilePath}")
                elif value == 1:
                    title = "选择一个链接进行下载:"
                    optionsReg = dict()
                    optionsReg.update({f"0:{self.originalDownloadUrl}":self.originalDownloadUrl})
                    optionsReg.update({f"1:https://ghproxy.com/{self.originalDownloadUrl}":f"https://ghproxy.com/{self.originalDownloadUrl}"})
                    optionsReg.update({f"2:https://github.moeyy.xyz/{self.originalDownloadUrl}":f"https://github.moeyy.xyz/{self.originalDownloadUrl}"})
                    optionsReg.update({f"3:https://github.tsukiyukimiyako.top/{self.originalDownloadUrl}":f"https://github.tsukiyukimiyako.top/{self.originalDownloadUrl}"})
                    option = questionary.select(title, list(optionsReg.keys())).ask()
                    url = optionsReg.get(option)
                    self.log.info(f"开始下载: {url}")
                    self.DownloadWithProgress(url, self.downloadFilePath)
                    self.log.info(f"下载完成: {url}")
                break
            except Exception as e:
                self.log.error(f"下载失败: {e}")
                title = "可选择直接重试,或重开程序尝试获取到其他下载链接,或关闭/开启VPN再进行尝试,或选择特定链接下载:"
                optionsReg = dict()
                optionsReg.update({f"0:直接重试":0})
                optionsReg.update({"1:选择特定链接下载":1})
                option = questionary.select(title, list(optionsReg.keys())).ask()
                value = optionsReg.get(option)


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

    def CoverFolder(self, isAssetsUpdate = False):
        while True:
            try:
                if os.path.exists(os.path.abspath("./assets")) and isAssetsUpdate:
                    shutil.rmtree(os.path.abspath("./assets"))
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

            response = requests.get(FastestMirror.GetGithubApiMirror("himesamanoyume","HotaruAssistant", 5), timeout=3)
            if response.status_code == 200:
                data = json.loads(response.text)
                for item in data:
                    if isCheckPreRelease:
                        data = item
                        break
                    else:
                        if not item["prerelease"]:
                            data = item
                            break
                    
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