import pyuac
from managers.logger_manager import logger
import sys
import os
from managers.config_manager import config
from managers.translate_manager import _

class Reg:
    def reg_export():
        try:
            # 保存完整的注册表
            logger.info("保存完整的注册表")
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 D:\MihoyoLogin\\temp\\temp-full.reg /y")
            # 删除所有注册表
            logger.info("删除所有注册表")
            os.system(f"cmd /C reg delete HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 /f")
            # 等待游戏启动并登录
            logger.info("等待游戏启动并登录")
            os.system(f"cmd /C start \"\" \"{config.game_path}\"")
            uid = input("输入uid:\n")
            input("登录完成后按回车进入下一步...\n")
            # end
            # 导出对应账号注册表
            logger.info("导出对应账号注册表")
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 D:\MihoyoLogin\starrail\\starrail-{uid}.reg /y")
            # 重新导入完整注册表
            logger.info("重新导入完整注册表")
            os.system(f"cmd /C reg import D:\MihoyoLogin\\temp\\temp-full.reg")
            logger.info("完成,你已可以Alt+F4退出游戏")
            config.want_register_accounts[uid] = {}
            config.want_register_accounts[uid]['email'] = config.want_register_accounts['111111111']['email']
            config.want_register_accounts[uid]['reg_path'] = f'D:\MihoyoLogin\starrail\\starrail-{uid}.reg'
            config.want_register_accounts[uid]['active_day'] = config.want_register_accounts['111111111']['active_day']

            temp_list = list()
            temp_list.append('Bronya')
            temp_list.append('Blade')
            temp_list.append('Jingliu')
            temp_list.append('JingYuan')

            config.want_register_accounts[uid]['universe_team'] = temp_list
            
            config.want_register_accounts[uid]['universe_fate'] = config.want_register_accounts['111111111']['universe_fate']
            config.want_register_accounts[uid]['universe_number'] = config.want_register_accounts['111111111']['universe_number']
            config.want_register_accounts[uid]['universe_difficulty'] = config.want_register_accounts['111111111']['universe_difficulty']
            config.save_config()
            config.save_config()

        except Exception as e:
            logger.error(f"发生错误: {e}")
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)

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
            Reg.reg_export()
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
        except KeyboardInterrupt:
            logger.error("发生错误: 手动强制停止")
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
        except Exception as e:
            logger.error(f"发生错误: {e}")
            input(_("按回车键关闭窗口. . ."))
            sys.exit(1)

