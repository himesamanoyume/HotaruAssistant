
def testFun():
    import socket
    print(socket.gethostname())

if __name__ == '__main__':
    testFun()
    # if not pyuac.isUserAdmin():
    #     try:
    #         pyuac.runAsAdmin(wait=False)
    #         sys.exit(0)
    #     except Exception:
    #         logger.error("管理员权限获取失败")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    # else:
    #     try:
    #         for i in range(10):
    #             testFun()
    #     except KeyboardInterrupt:
    #         logger.error("发生错误: 手动强制停止")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    #     except Exception as e:
    #         logger.error(f"发生错误: {e}")
    #         input("按回车键关闭窗口. . .")
    #         sys.exit(0)
    