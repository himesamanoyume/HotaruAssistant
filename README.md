<div>
<p>
    <img src="./assets/screenshot/Hotaru.png" align="right">
</p>

<h1>
流萤小助手<br>
HotaruAssistant

By: 姫様の夢
</h1>

基于March7thAssistant v1.6.2

原项目地址[https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

<p>
    <img alt="" src="https://img.shields.io/github/v/release/himesamanoyume/HotaruAssistant?style=flat-square&color=4096d8" />
    <img alt="" src="https://img.shields.io/github/downloads/himesamanoyume/HotaruAssistant/total?style=flat-square&color=f18cb9" />
</p>

</div>

## 声明

- Chinese Support Only
- 随缘更新,没有群,某些我未用到的功能很可能已被我破坏了代码结构已无法使用,不做修复
- 不回答任何问题,本质上是原项目经过本人改造过后的私人仓库进行了公开,代码业余水平,盛产屎山

## 功能对比

功能|原版|此版
--|--|--
**多账号支持**|&cross;|&check;
**遗器胚子识别**|&cross;|&check;(不支持模拟宇宙遗器)
清体力|&check;|&check;
每日实训|&check;|&check;
每日委托|&check;|&check;
历战余响|&check;|&check;
模拟宇宙|&check;|&check;(仅支持刷满积分)
忘却之庭|&check;|&cross;
虚构叙事|不知道|&cross;
锄大地|&check;|&cross;
消息推送|&check;|仅支持邮件
UI|QT客户端|WebUI
OBS录制|&cross;|&check;

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/himesamanoyume/Auto_Simulated_Universe) 项目(为我自己适配本项目所修改的fork)，锄大地功能已经剔除

## 注意事项

- 必须在**PC端**且通过使用 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html) 在后台以 `1920*1080` 分辨率连接用户并以**全屏**运行游戏（不支持HDR）
- 确保已安装Python 3.11.1及以上版本, 调用的模拟宇宙模块为源码运行

## 下载安装

前往 [Releases](https://github.com/himesamanoyume/HotaruAssistant/releases/latest) 下载

检测更新可以点击图形界面设置最底下的按钮，或双击 `Update.exe`

## 相关项目

HotaruAssistant 离不开以下开源项目的帮助：

- 原版三月七助手 [https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

- 原版模拟宇宙自动化 [https://github.com/CHNZYX/Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe)

- OCR文字识别 [https://github.com/hiroi-sora/PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)

## TODO

- 教程写明更清晰的使用步骤(从blog中移动)
- ~~遗器新增设为垃圾~~,以及分解时对垃圾的选择

## 低优先级

- 新增任务堆栈 以每天为单位 每新的一天获取最上层选项为今天的目标 支持插入删除，当列表只剩一个时无限循环。插入删除操作时，1选择要插入的任务2选择对应的位置3决定是插入到前面还是插入到后面，删除时直接选择对应的任务 删除
- 新增设置开启自动战斗继承和config项
- 当一个事件距离开始不超过1天时 记为新活动开始发送通知
- 支持两个深渊信息查看
- 补回录制时出现致命错误依旧发送视频附件
- Bug:最后一个账号如果抛出异常进入非正常退出流程,则会直接开始下一轮循环
- 模拟宇宙脚本中领取沉浸奖励点击的部分可以尝试进行检测
- 新增继续模拟宇宙（继续进度，结束并结算）