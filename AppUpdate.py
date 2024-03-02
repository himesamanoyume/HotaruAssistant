from packaging.version import parse
import subprocess,tempfile,shutil,psutil,json,sys,time,requests,os,urllib.request,concurrent.futures,questionary
from tqdm import tqdm
from urllib.parse import urlparse

class AppUpdate:
    def __init__(self, actualDownloadUrl=None):
        self.processName = ("Hotaru Assistant Client.exe", "Hotaru Assistant Register.exe", "Hotaru Assistant Server.exe", "Hotaru Assistant Update.exe")
        self.apiUrls = [
            "https://api.github.com/repos/himesamanoyume/himesamanoyume/releases/latest",
            "https://cdn.jsdelivr.net/gh/himesamanoyume/himesamanoyume@release/latest.json",
            "https://ghproxy.com/https://raw.githubusercontent.com/himesamanoyume/himesamanoyume/release/latest.json",
            "https://github.moeyy.xyz/https://raw.githubusercontent.com/himesamanoyume/himesamanoyume/release/latest.json",
        ]

        self.tempPath = tempfile.gettempdir()
        if actualDownloadUrl is None:
            self.GetDownloadUrl()
        else:
            self.actualDownloadUrl = actualDownloadUrl
            self.actualExtractFolderPath = os.path.join(self.tempPath, os.path.basename(self.actualDownloadUrl).rsplit(".", 1)[0])

        self.actualDownloadFilePath = os.path.join(self.tempPath, os.path.basename(self.actualDownloadUrl))
        self.coverFolderPath = os.path.abspath("./")

    def FindFastestMirror(self, mirrorUrls, timeout=5):
        def CheckMirror(mirrorUrl):
            try:
                startTime = time.time()
                response = requests.head(mirrorUrl, timeout=timeout, allow_redirects=True)
                endTime = time.time()
                if response.status_code == 200:
                    responseTime = endTime - startTime
                    # print(f"镜像: {urlparse(mirror_url).netloc} 响应时间: {response_time}")
                    return mirrorUrl
            except Exception:
                pass
            return None
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futureToMirror = {executor.submit(CheckMirror, mirrorUrl): mirrorUrl for mirrorUrl in mirrorUrls}

            for future in concurrent.futures.as_completed(futureToMirror):
                result = future.result()
                if result:
                    executor.shutdown()
                    # print(f"最快的镜像为: {urlparse(result).netloc}")
                    return result

        # print(f"测速失败，使用默认镜像：{urlparse(mirror_urls[0]).netloc}")
        return mirrorUrls[0]
    
    def GetDownloadUrl(self):
        print("开始检测更新")
        while True:
            try:
                with urllib.request.urlopen(self.FindFastestMirror(self.apiUrls), timeout=10) as response:
                    if response.getcode() == 200:
                        data = json.loads(response.read().decode('utf-8'))
                        break
                    print("检测更新失败")
            except urllib.error.URLError as e:
                print(f"检测更新失败: {e}")
            input("按回车键重试. . .")

        # 获取最新版本
        for asset in data["assets"]:
            if "Assets" in asset["browser_download_url"]:
                self.downloadAssetsUrl = asset["browser_download_url"]
                self.latestAssetsVersion = self.downloadAssetsUrl.split("HotaruAssistantAssets_")[1].split(".zip")[0]
                self.extractAssetsFolderPath = os.path.join(self.tempPath, os.path.basename(self.downloadAssetsUrl).rsplit(".", 1)[0])
                continue
            else:
                self.downloadHotaruUrl = asset["browser_download_url"]
                self.extractHotaruFolderPath = os.path.join(self.tempPath, os.path.basename(self.downloadHotaruUrl).rsplit(".", 1)[0])
                continue

        # 比较本地版本
        isLatestTxt = ""
        try:
            latestHotaruVersion = data["tag_name"]
            with open("./assets/config/version.txt", 'r', encoding='utf-8') as txtFile:
                self.currentHotaruVersion = txtFile.read()
                txtFile.close()
            with open("./assets/config/meta.json", 'r', encoding='utf-8') as jsonFile:
                self.currentAssetsVersion = json.loads(jsonFile)['hotaru_assets_version']
                jsonFile.close()

            if parse(latestHotaruVersion.lstrip('v')) > parse(self.currentHotaruVersion.lstrip('v')):
                print(f"发现助手新版本：{self.currentHotaruVersion} ——> {latestHotaruVersion}")
                self.actualDownloadUrl = self.downloadHotaruUrl
                self.actualExtractFolderPath = self.extractHotaruFolderPath
                isLatestTxt = "[检测到助手新版本,应选择更新]"
            else:
                print(f"当前助手已是最新版本: {self.currentAssetsVersion}, 开始检测资源版本")
                if parse(self.latestAssetsVersion.lstrip('v')) > parse(self.currentAssetsVersion.lstrip('v')):
                    print(f"发现资源新版本：{self.currentAssetsVersion} ——> {self.currentAssetsVersion}")
                    self.actualDownloadUrl = self.downloadAssetsUrl
                    self.actualExtractFolderPath = self.extractAssetsFolderPath
                    isLatestTxt = "[检测到资源新版本,应选择更新]"
                else:
                    print(f"当前已是最新版本: {self.currentAssetsVersion}")
        except Exception:
            print(f"本地版本获取失败\n最新助手版本: {latestHotaruVersion}, 最新资源版本: {self.latestAssetsVersion}")

        title = "选择进行更新/重新下载或退出更新:"
        optionsReg = dict()
        optionsReg.update({f"0:更新/重新下载 {isLatestTxt}":0})
        optionsReg.update({"1:退出程序":1})
        option = questionary.select(title, list(optionsReg.keys())).ask()
        value = optionsReg.get(option)
        if value == 0:
            # 设置镜像
            apiEndpoints = [
                self.actualDownloadUrl,
                f"https://ghproxy.com/{self.actualDownloadUrl}",
                f"https://github.moeyy.xyz/{self.actualDownloadUrl}",
            ]
            self.actualDownloadUrl = self.FindFastestMirror(apiEndpoints)
            self.actualExtractFolderPath = self.actualExtractFolderPath

            print(f"下载地址：{self.actualDownloadUrl}")
            input("按回车键开始更新")
        elif value == 1:
            sys.exit(0)

    def DownloadWithProgress(self, downloadUrl, savePath):
        # 获取文件大小
        response = urllib.request.urlopen(downloadUrl)
        fileSize = int(response.info().get('Content-Length', -1))

        # 使用 tqdm 创建进度条
        with tqdm(total=fileSize, unit='B', unitScale=True, unitDivisor=1024) as pbar:
            def UpdateBar(blockCount, blockSize, totalSize):
                if pbar.total != totalSize:
                    pbar.total = totalSize
                downloaded = blockCount * blockSize
                pbar.update(downloaded - pbar.n)

            urllib.request.urlretrieve(downloadUrl, savePath, reporthook=UpdateBar)

    def TerminateProcess(self):
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            for name in self.processName:
                if name in proc.info['name']:
                    try:
                        process = psutil.Process(proc.info['pid'])
                        process.terminate()
                        process.wait(timeout=10)
                    except (psutil.NoSuchProcess, psutil.TimeoutExpired, psutil.AccessDenied):
                        pass
    
    def DownloadFile(self):
        print("开始下载...")
        while True:
            try:
                self.DownloadWithProgress(self.actualDownloadUrl, self.actualDownloadFilePath)
                print(f"下载完成：{self.actualDownloadFilePath}")
                break
            except Exception as e:
                print(f"下载失败：{e}")
                input("按回车键重试. . .")

    def ExtractFile(self):
        print("开始解压...")
        while True:
            try:
                shutil.unpack_archive(self.actualDownloadFilePath, self.tempPath)
                print(f"解压完成：{self.actualExtractFolderPath}")
                break
            except Exception as e:
                print(f"解压失败：{e}")
                input("按回车键重试. . .")

    def CoverFolder(self):
        print("开始覆盖...")
        while True:
            try:
                shutil.copytree(self.actualExtractFolderPath, self.coverFolderPath, dirs_exist_ok=True)
                print(f"覆盖完成：{self.coverFolderPath}")
                break
            except Exception as e:
                print(f"覆盖失败：{e}")
                input("按回车键重试. . .")

    def DeleteFiles(self):
        print("开始清理...")
        try:
            os.remove(self.actualDownloadFilePath)
            print(f"清理完成：{self.actualDownloadFilePath}")
        except Exception as e:
            print(f"清理失败：{e}")
        try:
            shutil.rmtree(self.actualExtractFolderPath)
            print(f"清理完成：{self.actualExtractFolderPath}")
        except Exception as e:
            print(f"清理失败：{e}")

    def Run(self):
        print("开始终止进程...")
        self.TerminateProcess()
        print("终止进程完成")

        self.DownloadFile()

        self.ExtractFile()

        self.CoverFolder()

        self.DeleteFiles()

        input("按回车键关闭窗口")

def CheckTempDir():
    if not getattr(sys, 'frozen', False):
        print("更新程序只支持打包成exe后运行")
        sys.exit(1)

    tempPath = tempfile.gettempdir()
    filePath = os.path.abspath(sys.argv[0])
    fileName = os.path.basename(filePath)
    destinationPath = os.path.join(tempPath, fileName)

    if not filePath == destinationPath:
        while True:
            try:
                shutil.copy(filePath, os.path.join(tempPath, fileName))
                break
            except Exception as e:
                print(f"复制更新程序到临时目录失败：{e}")
                input("按回车键重试. . .")
        subprocess.run(["start", os.path.join(tempPath, fileName)] + sys.argv[1:], shell=True)
        sys.exit(0)


if __name__ == '__main__':
    CheckTempDir()

    if len(sys.argv) == 2:
        update = AppUpdate(sys.argv[1])
    else:
        update = AppUpdate()

    update.Run()