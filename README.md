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

- 新增.bat启动server
- 新增自动管理员启动OBS并检测是否存在进程
- 当模拟宇宙已满分时(universe_fin==true),没有清体力选为模拟宇宙的UID将跳过模拟宇宙轮次
- ~~config新增录屏enable,关闭后不带视频附件,不录屏~~
- ~~修改邮件脚本相关描述~~
- **新增如果每日未完成,不发送邮件**
- 模拟宇宙脚本中领取沉浸奖励点击的部分可以尝试
- 新增继续模拟宇宙（继续进度，结束并结算）
- 想办法远程操作config
- 想办法在screen之间做更快速的联动（优化）
- config save load用队列
- *task_mappings改成全部图片扫描*
- 新增换服脚本
- 新增一个py脚本专门用于修改config,flask?