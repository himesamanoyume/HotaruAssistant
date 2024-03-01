from Hotaru.Server.LogServerHotaru import logServerMgr
from Hotaru.Server.ConfigServerHotaru import configServerMgr
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
        return FastestMirror.FindFastestMirror(configServerMgr.mConfig.mConfigKey.common.pypi_mirror_urls, timeout)

    @staticmethod
    def FindFastestMirror(mirrorUrls, timeout=5):

        def CheckMirror(mirrorUrl):
            try:
                startTime = time.time()
                response = requests.head(mirrorUrl, timeout=timeout, allow_redirects=True)
                endTime = time.time()
                if response.status_code == 200:
                    response_time = endTime - startTime
                    logServerMgr.Info("镜像: {mirror} 响应时间: {time}").format(mirror=urlparse(mirrorUrl).netloc, time=response_time)
                    return mirrorUrl
            except Exception:
                pass
            return None
        
        logServerMgr.Info("开始测速")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futureToMirror = {executor.submit(CheckMirror, mirrorUrl): mirrorUrl for mirrorUrl in mirrorUrls}

            for future in concurrent.futures.as_completed(futureToMirror):
                result = future.result()
                if result:
                    executor.shutdown()
                    logServerMgr.Info("最快的镜像为: {mirror}").format(mirror=urlparse(result).netloc)
                    return result

        logServerMgr.Error("测速失败，使用默认镜像：{mirror}").format(mirror=urlparse(mirrorUrls[0]).netloc)
        return mirrorUrls[0]
