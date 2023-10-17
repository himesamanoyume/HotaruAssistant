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

## TODO

- 清除原作者的一些信息
- is_next_mon_4_am未做修改
- 历战余响每周检测未做修改
- 使用消耗品时似乎没有尝试重试
- **针对多账号存储不同的配置和记录**
- ~~last_run_timestamp也需要添加分账号配置~~
- ~~daily_tasks中如果有项目为False且没到第二天时,该项目不要一律更改为True~~
- ~~根据config中是否开启多账号选项,和multi_login_accounts的中的地址,将依次注入对应的注册表后才开始启动游戏,该账号结束后关闭游戏窗口,再注入下一注册表后才再启动游戏,列表全部完成后再根据对应选项收尾~~

## 功能简介

- **日常**：清体力、每日实训、领奖励、委托、锄大地
- **周常**：历战余响、模拟宇宙、忘却之庭
- 每日实训等任务的完成情况支持消息推送
- 凌晨四点或体力恢复到指定值后自动启动
- 任务完成后声音提示、自动关闭游戏或关机

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe) 项目，锄大地调用的 [Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail) 项目

详情见 [配置文件](assets/config/config.example.yaml) 或图形界面设置 ｜🌟喜欢就给个星星吧|･ω･) 🌟｜QQ群 [855392201](https://qm.qq.com/q/9gFqUrUGVq) TG群 [点击跳转](https://t.me/+ZgH5zpvFS8o0NGI1)

## 界面展示

![README](assets/screenshot/README.png)

## 注意事项

- 必须使用**PC端** `1920*1080` 分辨率窗口或全屏运行游戏（不支持HDR）
- 模拟宇宙相关 [项目文档](https://asu.stysqy.top/)  [Q&A](https://asu.stysqy.top/guide/qa.html)
- 需要后台运行或多显示器可以尝试 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html)
- 遇到错误请在 [Issue](https://github.com/moesnow/March7thAssistant/issues) 反馈，提问讨论可以在 [Discussions](https://github.com/moesnow/March7thAssistant/discussions) ，群聊随缘看，欢迎 [PR](https://github.com/moesnow/March7thAssistant/pulls)

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

如果喜欢本项目，可以微信赞赏送作者一杯咖啡☕

您的支持就是作者开发和维护项目的动力🚀

![sponsor](assets/screenshot/sponsor.jpg)

---

## 相关项目

March7thAssistant 离不开以下开源项目的帮助：

- 模拟宇宙自动化 [https://github.com/CHNZYX/Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe)

- 锄大地自动化 [https://github.com/linruowuyin/Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail)

- OCR文字识别 [https://github.com/hiroi-sora/PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)

- 图形界面组件库 [https://github.com/zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)


## Contributors
<a href="https://github.com/moesnow/March7thAssistant/graphs/contributors">

  <img src="https://contrib.rocks/image?repo=moesnow/March7thAssistant" />

</a>

## Stargazers over time

[![Star History](https://starchart.cc/moesnow/March7thAssistant.svg)](https://starchart.cc/moesnow/March7thAssistant)
