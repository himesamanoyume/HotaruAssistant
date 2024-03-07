from Hotaru.Server.LogServerHotaru import logMgr
from Hotaru.Server.ConfigServerHotaru import configMgr
from urllib.parse import urlparse
import requests, time
import concurrent.futures

class FastestMirror:
    @staticmethod
    def GetGithubMirror(downloadUrl, timeout=10):
        mirrorUrls = [
            downloadUrl,
            f"https://ghproxy.com/{downloadUrl}",
            f"https://github.moeyy.xyz/{downloadUrl}",
        ]
        return FastestMirror.FindFastestMirror(mirrorUrls, timeout)
    
    @staticmethod
    def GetGithubApiMirror(user, repo, file, timeout=5):
        mirrorUrls = [
            f"https://api.github.com/repos/{user}/{repo}/releases/latest",
            f"https://cdn.jsdelivr.net/gh/himesamanoyume/HotaruAssistant@release/{file}",
            f"https://ghproxy.com/https://raw.githubusercontent.com/himesamanoyume/HotaruAssistant/release/{file}",
            f"https://github.moeyy.xyz/https://raw.githubusercontent.com/himesamanoyume/HotaruAssistant/release/{file}",
        ]
        return FastestMirror.FindFastestMirror(mirrorUrls, timeout)
    
    @staticmethod
    def GetPypiMirror(timeout=5):
        return FastestMirror.FindFastestMirror(configMgr.mKey.PYPI_MIRROR_URLS, timeout)

    @staticmethod
    def FindFastestMirror(mirrorUrls, timeout=5):

        def CheckMirror(mirrorUrl):
            try:
                startTime = time.time()
                response = requests.head(mirrorUrl, timeout=timeout, allow_redirects=True)
                endTime = time.time()
                if response.status_code == 200:
                    responseTime = endTime - startTime
                    logMgr.Info(f"镜像: {urlparse(mirrorUrl).netloc} 响应时间: {responseTime}")
                    return mirrorUrl
            except Exception:
                pass
            return None
        
        logMgr.Info("开始测速")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futureToMirror = {executor.submit(CheckMirror, mirrorUrl): mirrorUrl for mirrorUrl in mirrorUrls}

            for future in concurrent.futures.as_completed(futureToMirror):
                result = future.result()
                if result:
                    executor.shutdown()
                    logMgr.Info(f"最快的镜像为: {urlparse(result).netloc}")
                    return result

        logMgr.Error(f"测速失败，使用默认镜像：{urlparse(mirrorUrls[0]).netloc}")
        return mirrorUrls[0]
