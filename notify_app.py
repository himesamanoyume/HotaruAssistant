from managers.notify_manager import notify
from managers.logger_manager import logger
import pyuac
import sys

def main():
    type = input("1:全体公告,2:单人通知\n")
    content = input("输入公告内容:\n")

    if type in ['1','2']:
        if type == '1':
            notify.announcement("HimeProducer - 公告", f"<p>{content}</p>")
        elif type == '2':
            notify.announcement("单人通知!", f"<p>{content}</p>", isSingle=True)

    input(("按回车键关闭窗口. . ."))
    sys.exit(1)

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        try:
            pyuac.runAsAdmin(wait=False)
            sys.exit(0)
        except Exception:
            logger.error(("管理员权限获取失败"))
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
    else:
        try:
            main(sys.argv[1]) if len(sys.argv) > 1 else main()
        except KeyboardInterrupt:
            logger.error(("发生错误: {e}").format(e=("手动强制停止")))
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
        except Exception as e:
            logger.error(("发生错误: {e}").format(e=e))
            # notify.notify(_("发生错误: {e}").format(e=e))
            input(("按回车键关闭窗口. . ."))
            sys.exit(1)
    

    