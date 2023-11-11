import winreg
import os

# key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f'Software\\miHoYo\\崩坏：星穹铁道')

# value = winreg.QueryValue(key, 'MIHOYOSDK_ADL_PROD_CN_h3123967166')

key = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
sub_key = "Software\\miHoYo\\崩坏：星穹铁道"
with winreg.OpenKey(key, sub_key) as reg_key:
    value, _ = winreg.QueryValueEx(reg_key, "MIHOYOSDK_ADL_PROD_CN_h3123967166")

print(value)
winreg.CloseKey(key)

# https://blog.51cto.com/u_16213364/7875395

# file_handler = logging.FileHandler(f"./logs/{self.current_datetime()}.log", encoding="utf-8")
#         file_formatter = logging.Formatter('|%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d| %(message)s')
#         file_handler.setFormatter(file_formatter)
#         self.logger.addHandler(file_handler)

# if not os.path.exists("D:/MihoyoLogin/starrail"):
#     os.makedirs("D:/MihoyoLogin/starrail")
#     shutil.copy("./config.yaml",f"./backup/starrail-{uid}.reg")