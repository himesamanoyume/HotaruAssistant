from Modules.Utils.FastestMirror import FastestMirror
from packaging.version import parse
import requests,json

class CheckVersion:

    @staticmethod
    def CheckVersion():
        try:
            with open("./assets/config/version.txt", 'r', encoding='utf-8') as txtFile:
                currentHotaruVersion = txtFile.read()
                txtFile.close()
            with open("./assets/config/meta.json", 'r', encoding='utf-8') as jsonFile:
                currentAssetsVersion = json.load(jsonFile)['hotaru_assets_version']
                jsonFile.close()

            # response = requests.get(FastestMirror.GetGithubApiMirror("himesamanoyume","himesamanoyume",1), timeout=3)
            # if response.status_code == 200:
            #     data = json.loads(response.text)
                

                # —————————————————————————————暂时注释———————————————————————————————

                # cls.latestHotaruVersion = data["tag_name"]
                # for asset in data["assets"]:
                #     if "Assets" in asset["browser_download_url"]:
                #         cls.downloadAssetsUrl = asset["browser_download_url"]
                #         cls.latestAssetsVersion = cls.downloadAssetsUrl.split("HotaruAssistantAssets_")[1].split(".zip")[0]
                #         break

                # ——————————————————————————————————————————————————————————————————

                latestHotaruVersion = "v2.0.0.alpha.0"
                downloadAssetsUrl = "https://github.com/himesamanoyume/himesamanoyume/releases/download/v2.0.0/HotaruAssistantAssets_v2.0.0.alpha.0-1.zip"
                latestAssetsVersion = downloadAssetsUrl.split("HotaruAssistantAssets_")[1].split(".zip")[0]

                # ——————————————————————————————————————————————————————————————————

                # 比较本地版本
                isLatestTxt = ""
                isNeedUpdate = False

                if parse(latestHotaruVersion.lstrip('v')) > parse(currentHotaruVersion.lstrip('v')):
                    isLatestTxt = f"发现助手新版本：{currentHotaruVersion} ——> {latestHotaruVersion}"
                    isNeedUpdate = True
                else:
                    if parse(latestAssetsVersion.lstrip('v')) > parse(currentAssetsVersion.lstrip('v')):
                        isLatestTxt = f"发现资源新版本：{currentAssetsVersion} ——> {latestAssetsVersion}"
                        isNeedUpdate = True
                    else:
                        isLatestTxt = f"当前助手和资源包皆已是最新版本: {currentAssetsVersion}, {currentAssetsVersion}"

                return isLatestTxt, isNeedUpdate
            # else:
            #     isLatestTxt = f"检测更新失败: {response.text}"
            #     return isLatestTxt, False
        except Exception as e:
            isLatestTxt = f"检测更新失败:{e}"
            return isLatestTxt, False