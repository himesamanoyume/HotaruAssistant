import winreg
import json
import time
import pyuac
from managers.logger_manager import logger
import sys
from managers.translate_manager import _

class Reg:
    key = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    sub_key = "Software\\miHoYo\\崩坏：星穹铁道"
    value_name = "MIHOYOSDK_ADL_PROD_CN_h3123967166"
    reg_path = "D:\\MihoyoLogin\\starrail\\reg.json"
    
    def export_reg():
        try:
            print("进行注册表导出\n")
            uid = int(input("输入UID:\n"))

            

            with winreg.OpenKey(Reg.key, Reg.sub_key) as reg_key:
                get_value, _ = winreg.QueryValueEx(reg_key, Reg.value_name)
                real_value = str(get_value).split("'")[1]

            with open(Reg.reg_path, 'r', encoding='utf-8') as file:
                json_file_data = json.load(file)

            for data in json_file_data:
                if f"{uid}" in data:
                    data[f'{uid}'] = real_value
                    with open(Reg.reg_path, 'w') as file:
                        json.dump(json_file_data, file)
                    winreg.CloseKey(Reg.key)
                    print("检测到json中已有该uid,已更新reg_value")
                    return
                
            new_reg = {
                uid: real_value
            }
            json_file_data.append(new_reg)
            print("新uid,已新增reg_value")

            with open(Reg.reg_path, 'w') as file:
                json.dump(json_file_data, file)

            winreg.CloseKey(Reg.key)

        except FileNotFoundError:
            nowtime = time.time()
            raise Exception (f"{nowtime},配置文件不存在：{Reg.reg_path}")
        except Exception as e:
            nowtime = time.time()
            raise Exception (f"{nowtime},配置文件解析失败：{e}")

    def import_reg(uid):
        try:
            with winreg.OpenKey(Reg.key, Reg.sub_key) as reg_key:
                reg_path = "D:\\MihoyoLogin\\starrail\\reg.json"

            with open(reg_path, 'r', encoding='utf-8') as file:
                json_file_data = json.load(file)
                for data in json_file_data:
                    if f"{uid}" in data:
                        reg_value = data[f"{uid}"]
                        byte_value = bytearray(reg_value, 'utf-8')
                        winreg.SetValueEx(reg_key, Reg.value_name, 0, winreg.REG_BINARY, byte_value)
                        print(f"{uid}的reg_value已导入")
                        break
                            

            winreg.CloseKey(Reg.key)
                
        except FileNotFoundError:
            nowtime = time.time()
            raise Exception (f"{nowtime},配置文件不存在：{reg_path}")
        except Exception as e:
            nowtime = time.time()
            raise Exception (f"{nowtime},配置文件解析失败：{e}")

if __name__ == '__main__':
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logger.error(_("管理员权限获取失败"))
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
    else:
        try:
            Reg.export_reg()
            # Reg.import_reg(100193509)
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error(_("发生错误: {e}").format(e=_("手动强制停止")))
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
        except Exception as e:
            logger.error(_("发生错误: {e}").format(e=e))
            # notify.notify(_("发生错误: {e}").format(e=e))
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)
    # Reg.export_reg()
    # Reg.import_reg(100193509)
# https://blog.51cto.com/u_16213364/7875395