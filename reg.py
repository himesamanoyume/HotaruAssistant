from managers.logger_manager import logger
from managers.automation_manager import auto
from managers.screen_manager import screen
import sys,pyuac,os,questionary
from module.config.config import Config
from managers.translate_manager import _
from tasks.base.resolution import Resolution

class Reg:
    def main():
        logger.warning("在进行选择前,需要先手动把游戏退出!!!然后检查config.yaml中的game_path是否正确填入")
        title_ = "若已经关闭游戏,用方向键然后回车键选择你要做的:"
        options_reg = dict()
        options_reg.update({"选择获取新的注册表(会重新启动游戏,因此需要提前关闭游戏)":0})
        options_reg.update({"选择重新导入完整注册表(导入注册表后需要重启游戏才会生效)":1})
        option_ = questionary.select(title_, list(options_reg.keys())).ask()
        value = options_reg.get(option_)
        if value == 0:
            Reg.reg_export()
        elif value == 1:
            Reg.restore_reg()

    def restore_reg():
        logger.info("重新导入完整注册表")
        config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
        os.system(f"cmd /C reg import ./reg/temp-full.reg")

    def reg_export():
        try:
            config = Config("./assets/config/version.txt", "./assets/config/config.example.yaml", "./config.yaml")
            # 保存完整的注册表
            logger.info("保存完整的注册表")
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 ./reg/temp-full.reg /y")
            # 删除所有注册表
            logger.info("删除所有注册表")
            os.system(f"cmd /C reg delete HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 /f")
            # 等待游戏启动并登录
            logger.info("等待游戏启动并登录")
            os.system(f"cmd /C start \"\" \"{config.game_path}\"")

            logger.info("此时登录账号并点击进入游戏,之后等待加载至主界面,同时将分辨率调整至1920*1080...")
            input("是否已完成加载到主界面?若完成则按回车进入下一步开始识别UID...")

            Resolution.check(config.game_title_name, 1920, 1080)
            
            logger.info("正在自动识别UID")

            screen.change_to("main")

            uid = auto.get_single_line_text(crop = (70.0 / 1920, 1039.0 / 1080, 93.0 / 1920, 27.0 / 1080), blacklist=[], max_retries=9)

            options_reg2 = dict()
            options_reg2.update({f"正确,直接导出":0})
            options_reg2.update({"错误,手动输入UID":1})
            option_ = questionary.select(f"识别UID:{uid},是否正确?根据情况选择下列选项:", list(options_reg2.keys())).ask()
            value = options_reg2.get(option_)
            if value == 0:
                pass
            elif value == 1:
                uid = input("手动输入UID:\n")
            # end
            # 导出对应账号注册表
            logger.info("导出对应账号注册表")
            os.system(f"cmd /C reg export HKEY_CURRENT_USER\Software\miHoYo\崩坏：星穹铁道 ./reg/starrail-{uid}.reg /y")
            # 重新导入完整注册表
            logger.info("重新导入完整注册表")
            os.system(f"cmd /C reg import ./reg/temp-full.reg")
            logger.info("完成,你已可以退出游戏")
            config.want_register_accounts[uid] = {}
            config.want_register_accounts[uid]['email'] = config.want_register_accounts['111111111']['email']
            config.want_register_accounts[uid]['reg_path'] = f'./reg/starrail-{uid}.reg'
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

        except Exception as e:
            logger.error(f"发生错误: {e}")
            input("按回车键关闭窗口. . .")
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
            if not os.path.exists("./reg"):
                os.mkdir("./reg")
            Reg.main()
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

