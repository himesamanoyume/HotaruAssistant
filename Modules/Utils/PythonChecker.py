from Hotaru.Server.UpdateHotaru import updateMgr
from Hotaru.Server.LogServerHotaru import logMgr
from Hotaru.Server.ConfigServerHotaru import configMgr
from Modules.Utils.Command import Command
from Modules.Utils.GameWindow import GameWindow
from packaging.version import parse
import subprocess,tempfile,sys,os

class PythonChecker:
    @staticmethod
    def Run():
        if configMgr.mConfig[configMgr.mKey.PYTHON_EXE_PATH] != '' and PythonChecker.Check(configMgr.mConfig[configMgr.mKey.PYTHON_EXE_PATH]):
            return
        else:
            paths = Command.SubprocessWithStdout(["where", "python.exe"])
            if paths is not None:
                for path in paths.split("\n"):
                    if PythonChecker.Check(path):
                        configMgr.mConfig.SetValue(configMgr.mKey.PYTHON_EXE_PATH, path)
                        logMgr.Debug(f"Python 路径更新成功：{path}")
                        return

        logMgr.Warning("没有在环境变量中找到可用的 Python 路径")
        logMgr.Warning("如果已经修改了环境变量，请尝试重启程序，包括图形界面")
        logMgr.Warning("可以通过在 cmd 中输入 python -V 自行判断是否成功")
        logMgr.Warning("也可卸载后重新运行或在 config.yaml 中手动修改 python_exe_path")
        input("按回车键开始自动安装 Python 3.11.5 64bit")

        PythonChecker.Install()

    @staticmethod
    def Install():
        download_url = "http://mirrors.huaweicloud.com/python/3.11.5/python-3.11.5-amd64.exe"
        download_file_path = os.path.join(tempfile.gettempdir(), os.path.basename(download_url))
        destination_path = os.path.join(os.getenv('LocalAppData'), r'Programs\Python\Python311\python.exe')

        while True:
            try:
                os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
                logMgr.Info(f"开始下载：{download_url}")
                updateMgr.mUpdate.DownloadWithProgress(download_url, download_file_path)
                logMgr.Info(f"下载完成：{download_file_path}")
                break
            except Exception as e:
                logMgr.Error(f"下载失败：{e}")
                input("按回车键重试. . .")

        while True:
            try:
                if not subprocess.run(f"{download_file_path} /passive InstallAllUsers=0 PrependPath=1 Include_launcher=0 Include_test=0", shell=True, check=True):
                    raise Exception
                logMgr.Info("安装完成")
                break
            except Exception as e:
                logMgr.Error(f"安装失败：{e}")
                input("按回车键重试. . .")

        try:
            os.remove(download_file_path)
            logMgr.Info(f"清理完成：{download_file_path}")
        except Exception as e:
            logMgr.Error(f"清理失败：{e}")

        if PythonChecker.Check(destination_path):
            configMgr.mConfig.SetValue(configMgr.mKey.PYTHON_EXE_PATH, destination_path)
            PythonChecker.CheckAndSwitch(configMgr.mConfig[configMgr.mKey.GAME_TITLE_NAME])
            return

        logMgr.Info("安装完成，请重启程序，包括图形界面")
        input("按回车键关闭窗口. . .")
        sys.exit(0)

    @staticmethod
    def CheckAndSwitch(title):
        return GameWindow.SwitchToWindow(title, maxRetries=4)

    @staticmethod
    def Check(path):
        # 检查 Python 和 pip 是否可用
        python_result = Command.SubprocessWithStdout([path, '-V'])
        if python_result is not None and python_result[0:7] == "Python ":
            python_version = python_result.split(' ')[1]
            if parse(python_version) < parse("3.7"):
                logMgr.Error(f"Python 版本过低: {python_version} < 3.7")
                return False
            else:
                logMgr.Debug(f"Python 版本: {python_version}")
                python_arch = Command.SubprocessWithStdout([path, '-c', 'import platform; print(platform.architecture()[0])'])
                logMgr.Debug(f"Python 架构: {python_arch}")
                if "32" in python_arch:
                    logMgr.Error("不支持 32 位 Python")
                    return False
            pip_result = Command.SubprocessWithStdout([path, "-m", "pip", '-V'])
            if pip_result is not None and pip_result[0:4] == "pip ":
                pip_version = pip_result.split(' ')[1]
                logMgr.Debug(f"pip 版本: {pip_version}")
                return True
            else:
                logMgr.Debug(f"开始安装 pip")
                from Modules.Utils.FastestMirror import FastestMirror
                if subprocess.run([path, ".\\assets\\config\\get-pip.py", "-i", FastestMirror.GetPypiMirror()], check=True):
                    logMgr.Debug("pip 安装完成")
                    return True
                else:
                    logMgr.Error("pip 安装失败")
                    return False
        return False
