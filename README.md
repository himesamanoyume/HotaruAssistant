<div>
<p>
    <img src="./assets/screenshot/March7th.png" align="right">
</p>

<h1>
三月七小助手<br>
March7thAssistant - 私人版

By: 姫様の夢
</h1>

原项目地址[https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

<p>
    <img alt="" src="https://img.shields.io/github/v/release/himesamanoyume/himesamanoyume?style=flat-square&color=4096d8" />
    <img alt="" src="https://img.shields.io/github/downloads/himesamanoyume/himesamanoyume/total?style=flat-square&color=f18cb9" />
</p>

</div>

## TODO

- ~~Bug:模拟宇宙首周开启时无法正常识别到分数~~
- ~~新增选项允许开启5星遗器分解~~
- ~~分离出截屏功能,最终彻底抛弃appQt~~
- 补回录制时出现致命错误依旧发送视频附件

## 低优先级

- webui显示log
- Bug:最后一个账号若非正常退出,则会直接开始下一轮循环
- 模拟宇宙脚本中领取沉浸奖励点击的部分可以尝试进行检测
- 新增继续模拟宇宙（继续进度，结束并结算）
- 想办法在screen之间做更快速的联动（优化）

## 功能简介

- **日常**：清体力、每日实训、领奖励、委托、锄大地
- **周常**：历战余响、模拟宇宙、忘却之庭
- 每日实训等任务的完成情况支持消息推送
- 凌晨四点或体力恢复到指定值后自动启动
- 任务完成后声音提示、自动关闭游戏或关机

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/himesamanoyume/Auto_Simulated_Universe) 项目(也是我自己为适配本项目所修改的fork)，锄大地调用的 [Fhoe-Rail](https://github.com/himesamanoyume/Fhoe-Rail) 项目(也是我自己为适配本项目所修改的fork)

然而,锄大地功能已经剔除

详情见 [配置文件](assets/config/config.example.yaml) 或图形界面设置 

## 注意事项

- 必须使用**PC端** `1920*1080` 分辨率窗口或全屏运行游戏（不支持HDR）
- 需要后台运行或多显示器可以尝试 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html)

## 下载安装

前往 [Releases](https://github.com/himesamanoyume/himesamanoyume/releases/latest) 下载

检测更新可以点击图形界面设置最底下的按钮，或双击 `Update.exe`

## 相关项目

March7thAssistantPrivate 离不开以下开源项目的帮助：

- 原版三月七助手 [https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

- 原版模拟宇宙自动化 [https://github.com/CHNZYX/Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe)

- 原版锄大地自动化 [https://github.com/linruowuyin/Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail)

- OCR文字识别 [https://github.com/hiroi-sora/PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)

- 图形界面组件库 [https://github.com/zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)