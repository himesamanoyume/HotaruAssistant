<div align="center">
<p>
    <img src="./assets/screenshot/March7th.png">
</p>

<h1>
三月七小助手<br>
March7thAssistant
</h1>

<p>
    <img alt="" src="https://img.shields.io/badge/platform-Windows-blue?style=flat-square&color=4096d8" />
    <img alt="" src="https://img.shields.io/github/last-commit/moesnow/March7thAssistant?style=flat-square&color=f18cb9" />
    <img alt="" src="https://img.shields.io/github/v/release/moesnow/March7thAssistant?style=flat-square&color=4096d8" />
    <img alt="" src="https://img.shields.io/github/downloads/moesnow/March7thAssistant/total?style=flat-square&color=f18cb9" />
</p>

**简体中文** | [繁體中文](./README_TW.md) | [English](./README_EN.md)

快速上手，请访问：[使用教程](https://moesnow.github.io/March7thAssistant/#/assets/docs/Tutorial)

遇到问题，请在提问前查看：[FAQ](https://moesnow.github.io/March7thAssistant/#/assets/docs/FAQ)

</div>

## 功能简介

- **日常**：清体力、每日实训、领奖励、委托、锄大地
- **周常**：历战余响、模拟宇宙、忘却之庭
- 每日实训等任务的完成情况支持消息推送
- 凌晨四点或体力恢复到指定值后自动启动
- 任务完成后声音提示、自动关闭游戏或关机

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe) 项目，锄大地调用的 [Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail) 项目

详情见 [配置文件](assets/config/config.example.yaml) 或图形界面设置 

## 界面展示

![README](assets/screenshot/README1.png)

## 注意事项

- 必须使用**PC端** `1920*1080` 分辨率窗口或全屏运行游戏（不支持HDR）
- 模拟宇宙相关 [项目文档](https://asu.stysqy.top/)  [Q&A](https://asu.stysqy.top/guide/qa.html)
- 需要后台运行或多显示器可以尝试 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html)
- 遇到错误请在 [Issue](https://github.com/moesnow/March7thAssistant/issues) 反馈，提问讨论可以在 [Discussions](https://github.com/moesnow/March7thAssistant/discussions)

## 下载安装

前往 [Releases](https://github.com/moesnow/March7thAssistant/releases/latest) 下载后解压双击三月七图标的 `March7th Launcher.exe` 打开图形界面

如果需要使用 **任务计划程序** 定时运行或直接执行 **完整运行**，可以使用终端图标的 `March7th Assistant.exe`

检测更新可以点击图形界面设置最底下的按钮，或双击 `Update.exe`

## 源码运行

如果你是完全不懂的小白，请通过上面的方式下载安装，不用往下看了。

```cmd
git clone https://github.com/moesnow/March7thAssistant
cd March7thAssistant
pip install -r requirements.txt
python app.py
python main.py
```

<details>
<summary>开发相关</summary>

获取 crop 参数表示的裁剪坐标可以通过图形界面设置内的捕获截图功能

python main.py 后面支持参数 fight/universe/forgottenhall 等

</details>

---

## 相关项目

March7thAssistant 离不开以下开源项目的帮助：

- 模拟宇宙自动化 [https://github.com/CHNZYX/Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe)

- 锄大地自动化 [https://github.com/linruowuyin/Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail)

- OCR文字识别 [https://github.com/hiroi-sora/PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)

- 图形界面组件库 [https://github.com/zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

## TODO

- 深渊也要有二倍速识别
- alt f4关闭游戏时要确保切到了游戏 研究如何确定是否切到游戏
- 研究子程序进行中能不能切回来再回去
- 当花费时长超40分钟时将该账号并列入黑名单,邮件单独通知我
- ~~遗器胚子词条似乎不够完善(主生命,单暴3词条没锁?主爆伤3没用词条没锁)~~
- - ~~新增根据遗器部位单独判断胚子~~
- ~~识别遗器时还是要logger出主副词条~~
- ~~研究循环流程~~
- 循环流程新增while True下,for循环前的首次启动时间戳,如设置12小时,当for循环结束后判断当前时间是否超过12小时的限制,若超过则直接重新开始循环,若不到12小时则计算剩余时间并sleep()。如果12小时后超过凌晨4点,则以4点为启动时间
- 研究进程PID用于退出游戏/实在不行可使用alt+f4或正常退出游戏
- 模拟宇宙开始前检查时间戳,如果为0,说明可能没选择过角色与第几宇宙和难度,则先选好角色、难度、宇宙进入一遍再退出,再进行3rdparty
- - 如果时间戳不为0,且需要进行模拟宇宙时,先检查当前所选的角色、难度、宇宙是否与配置相同
- **长期评估account_active正确性**
- 加入顶号处理 掉线处理
- 领取每日活跃度时有些任务名识别不出来 比如**累计触发弱点击破5次**
- 通过qq机器人实现用户注册:用户私聊获知账号密码和验证码接收,以及配置的修改,注册需要填写单号,经过我审核通过,然后通过脚本实现注册表的获取
- 研究国服国际服切换
- daily_memory_one_team测试是否能写入超出4个角色的候补
- Bug:远程桌面多开，一个用户打完了会关闭其他用户进程


