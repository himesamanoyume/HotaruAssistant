import os,sys,subprocess

if __name__ == "__main__":
    version_txt = open("./assets/config/version.txt", "r", encoding='utf-8')
    version = version_txt.read()
    version_txt.close()

    command1 = ["pyinstaller", "main.py", "-D", "--distpath", f".\dist\M7A_Private", "-i","./assets/logo/March7th.ico", "--contents-directory", "libraries", "--exclude-module", "PyQt5", "--uac-admin", "-n", "March7th Assistant Client", "--onefile", "-y"]
    subprocess.run(command1, shell=True, stdout=True)

    command2 = ["pyinstaller", "reg.py", "-D", "--distpath", f".\dist\M7A_Private", "-i","./assets/logo/Terminal.ico", "--contents-directory", "libraries", "--exclude-module", "PyQt5", "--uac-admin", "-n", "March7th Assistant Register", "--onefile", "-y"]
    subprocess.run(command2, shell=True, stdout=True)

    command3 = ["pyinstaller", "server.py", "-D", "--distpath", f".\dist\M7A_Private", "-i","./assets/logo/Terminal.ico", "--contents-directory", "libraries", "--exclude-module", "PyQt5", "--uac-admin", "-n", "March7th Assistant Server", "--onefile", "--add-data=templates;templates", "--add-data=static;static", "-y"]
    subprocess.run(command3, shell=True, stdout=True)

    command4 = ["pyinstaller", "update.py", "-D", "--distpath", f".\dist\M7A_Private", "-i","./assets/logo/Update.ico", "-n", "Update", "--onefile", "-y"]
    subprocess.run(command4, shell=True, stdout=True)

    os.system(f"xcopy /E /I /Y .\\assets\ .\dist\M7A_Private\\assets\\")

    # os.system(f"xcopy /E /I /Y .\\static\ .\dist\M7A_Private\\static\\")

    os.system(f"xcopy /Y .\README.md .\dist\M7A_Private\\")

    os.system(f"xcopy /Y .\static\css\common.css .\dist\M7A_Private\\assets\\css")

    os.system(f"powershell Compress-Archive -Path .\dist\M7A_Private\ -DestinationPath .\dist\M7A_Private_{version}.zip -Force")

    input("按回车键退出...")
    sys.exit(0)
