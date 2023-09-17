from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QSize

from qfluentwidgets import NavigationItemPosition, MSFluentWindow, SplashScreen, setThemeColor, NavigationBarPushButton, toggleTheme, setTheme, darkdetect, Theme
from qfluentwidgets import FluentIcon as FIF

from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from .tasks_interface import TasksInterface
from .changelog_interface import ChangelogInterface
from .fqa_interface import FQAInterface

from .card.messagebox3 import MessageBox3

from managers.config_manager import config
from .tools.check_update import checkUpdate
from .tools.disclaimer import disclaimer


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK if darkdetect.theme() == 'Dark' else Theme.LIGHT)
        # setTheme(Theme.DARK)
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.tasksInterface = TasksInterface(self)
        self.settingInterface = SettingInterface(self)
        self.changelogInterface = ChangelogInterface(self)
        self.fqaInterface = FQAInterface(self)

        self.initNavigation()
        self.splashScreen.finish()

        if not config.agreed_to_disclaimer:
            disclaimer(self)

        if config.check_update:
            checkUpdate(self)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('主页'))
        self.addSubInterface(self.tasksInterface, FIF.LABEL, self.tr('每日实训'))
        self.addSubInterface(self.changelogInterface, FIF.UPDATE, self.tr('更新日志'))
        self.addSubInterface(self.fqaInterface, FIF.CHAT, self.tr('常见问题'))
        # self.navigationInterface.addSeparator()

        self.navigationInterface.addWidget(
            'themeButton',
            NavigationBarPushButton(FIF.BRUSH, '主题', isSelectable=False),
            self.toggleTheme,
            NavigationItemPosition.BOTTOM)

        self.navigationInterface.addWidget(
            'avatar',
            NavigationBarPushButton(FIF.HEART, '赞赏', isSelectable=False),
            self.onSupport,
            NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('设置'), position=NavigationItemPosition.BOTTOM)

    def toggleTheme(self):
        toggleTheme(save=False)

    def initWindow(self):
        # 禁用最大化
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)
        # self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

        setThemeColor('#f18cb9')

        self.resize(960, 780)
        self.setWindowIcon(QIcon('assets\logo\March7th.ico'))
        self.setWindowTitle("March7th Assistant")

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        w = MessageBox3(
            '支持作者🥰',
            '如果喜欢本项目，可以微信赞赏送作者一杯咖啡☕\n您的支持就是作者开发和维护项目的动力🚀',
            './assets/app/images/sponsor.jpg',
            self
        )
        w.yesButton.setText('下次一定')
        w.cancelButton.setHidden(True)
        w.exec()
