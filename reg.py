import winreg
import json
import time

# key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f'Software\\miHoYo\\崩坏：星穹铁道')

# value = winreg.QueryValue(key, 'MIHOYOSDK_ADL_PROD_CN_h3123967166')

key = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
sub_key = "Software\\miHoYo\\崩坏：星穹铁道"
with winreg.OpenKey(key, sub_key) as reg_key:
    get_value, _ = winreg.QueryValueEx(reg_key, "MIHOYOSDK_ADL_PROD_CN_h3123967166")

with winreg.OpenKey(key, sub_key, 0, winreg.KEY_ALL_ACCESS) as reg_key:
    write_value = "GbQh2g7VEn4yo6MJ6hsJ9mWm/WwvAMdvPC7GidvriUelrFkYgUhW15k/Y6fbus54EJBIV83F9IO4vnm949L5a6vAnlCELYWpGbzxawn0OTaXNpCj4QfK/kjnSU+x72gFAseYqTR1imystNWj6FBVUWynxFf2OaNXLXQTb6K+ldqk6vCmR8+2FaHFK3Dxo5/nATdBSwCPIxMvB1fkdDAIXlLCVWWu1DilhLkOS6ZE5U17ves07uhcgXu/mNcSdnwA8KPGAgwz4hzPvwFIIpRYD3XVHRrONmhYyCforUHD9cUkMCMx6y8116+FAozgNqbV3jXAtTXfzWq1nplF8gZb7xAaySFiD+eWXCbbO+6jlRJwUEIOGb4AVKXFKOn20Icc8qWDbevNL0GD++hn3VtYc9/BJVOAaD0YIPcwqSiw783pFRi65QoOnlpDdqMjsh4wXdtjJDJIlAJXIqUa34DRiE6tRK0NaZmSyBfbdThjZzqwxVYUN2PlguivK2/z75RnXo2Mog3n2XUj39PjubqHuUxC4J7jLXIxIpZKuaYE8v2y6MxIG0RCH1aweMUf8G1MKCxdLUcPfJJ3SyTPi6xCylPNoU+VKXmFS8vpnHRjryJN3jxRQANT5Nmxa7QeJCvIQ4L+KeCW0BHXUI0ZNV/LVLgw4EzperLvnPEbb7wA7TMJ00+EJikFSIIpl6C82tGPTMEsTn9MC02Pr2nyfoANs+Pqiq78owRbEtg46UsTGKBVzM6y8NUyBTzg5J8UmjGuBgsC9dAHWtWeKf5ReqvKw8HZv8Ibt1hwYKw5w9svDDID3ArxvYPlUPpH0nFKYpwAYFdfRmuAsX/ensIm3hkxWsDuhXpsGM+ny01Yj743Xa9ddAGcZhuMM+9jvCP49Z/H07TPvPkLCn0nINEVxyUZYOoX/e6zluh8dH20LVvasaf5lyJSC/mkR7dlAj9o23RnrFyw5YjSU6+7/C5GrMgezDK2Btq+yXeUwk+qIlxCaOnOQwO+DQtTGjfVzMClKy2yyYeSrAKpnJ3JC09sNJz8uQ28Nk5VfJ1tEjWt/rJCRoYXpUwIDnAIEE32o+YbBwSd4J9VT5K+t8UqB9FACDuPMhnY7Kq1hZ8COCwCFKS13O0FkAIklBiHY5KkEIAEhTRxGW+bREU59NnebZ90HST6gqDC21gp2JuTXOLbV1hl3RcpoYcByfqHQEHzaaRq8xH8yfBkDTMvWoIX4deKAW02neSkVgaF4kMec8Tq1OmuzRNvpJoWYpyDpVmgSYQXbZpIxnynN2sY089dPPkxevgfb4UJUqs46D6S34ABcs6Ocb8knGOKPBk8FML+W8wuRrkYbtgRCIVcr9ayKWsKdud+Azkuq3s+c/bU+fjYsf3BC0MIsZVdLdfiPPvOsUwiTy/BxR7HmO42aRyZbQjWoW1d9nTZ0Gr+J/xMJPQNCoUvtcK8iRuWMR86uQTetuQyzmEs3330enpryTC3fagKYvAzHHDD70mH7AN38SxhfjoNZ/BBDWJiIGNSX8WOP5YqvswojlNL/NbgZXKl8ry3s4qbaOieWmrQWdiX\x00"
    # print(write_value)
    value = bytearray(write_value, 'utf-8')
    winreg.SetValueEx(reg_key, "MIHOYOSDK_ADL_PROD_CN_h3123967166", 0, winreg.REG_BINARY, value)

try:
    reg_path = "D:\\MihoyoLogin\\starrail\\reg.json"
    with open(reg_path, 'r', encoding='utf-8') as file:
        for config in json.load(file):
            id = config["id"]
except FileNotFoundError:
    nowtime = time.time()
    raise Exception (f"{nowtime},配置文件不存在：{reg_path}")
except Exception as e:
    nowtime = time.time()
    raise Exception (f"{nowtime},配置文件解析失败：{e}")

# print(value)
winreg.CloseKey(key)

# https://blog.51cto.com/u_16213364/7875395