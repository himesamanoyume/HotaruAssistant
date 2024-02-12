<div>
<p>
    <img src="./assets/screenshot/Hotaru.png" align="right">
</p>

<h1>
HotaruAssistant · 流萤小助手<br>
</h1>

<h6>三月七你别再联系了,我怕流萤误会</h6>

基于March7thAssistant v1.6.2

原项目地址[https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

<p>
    <img alt="" src="https://img.shields.io/github/v/release/himesamanoyume/HotaruAssistant?style=flat-square&color=4096d8" />
    <img alt="" src="https://img.shields.io/github/downloads/himesamanoyume/HotaruAssistant/total?style=flat-square&color=f18cb9" />
</p>

</div>

# 协议通过, 开启焦土作战

- 指重构项目

由于当初使用这个项目时本意只是稍微改改一些功能来符合我个人的使用习惯,因此代码写得十分随意,而且在这之前没有系统学习过python,直接从别的语言靠经验转过来,想写什么逻辑直接对应着去查python怎么写就怎么写了,因此这也是我觉得我这代码很屎山的主要原因

之后随着我越来越多地依据自身需求进行改造,同时也由于崩铁不像原神那样一成不变地积极优化,我开始觉得开发过程变得越来越麻烦

而且本项目也与原版三月七助手的代码差别开始越来越大,我已经完全不同步原版项目的更新了,因此在本项目适配崩铁2.0版本基本完善之后,我决定对本项目进行龟速的重构

> 我将...点燃大海!

以应对不断变化的崩铁自动化流程,同时也提高项目可维护性

原版三月七助手的2.0版本早已上线,而此项目的2.0版本将在重构完成后到来

> 等回到现实,记得告诉所有人,是星核猎手送了你们最后一程。

## 声明

- Chinese Support Only
- 随缘更新,没有群,不写Changelog,某些我未用到的功能很可能已被我破坏了代码结构已无法使用,除非影响到了我使用否则不做修复,有能力建议自己改
- 不回答任何问题,本质上是原项目经过本人改造过后的私人仓库进行了公开,业余水平,盛产屎山

## 功能对比

功能|原版|此版
--|--|--
**多账号支持**|&cross;|&check;
**遗器胚子识别**|&cross;|&check;(不支持模拟宇宙遗器)
**遗器自动分解**|&cross;|&check;
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

> 本项目用于在一个后台用户上完成所有账号的日常周常,若有锄大地等需求建议使用[原版三月七助手](https://github.com/moesnow/March7thAssistant)每个账号开一个用户单独运作,或者直接单独使用原项目仓库中提到的[原版模拟宇宙自动化](https://github.com/CHNZYX/Auto_Simulated_Universe)和[原版锄大地自动化](https://github.com/linruowuyin/Fhoe-Rail)项目

## 下载安装

前往 [Releases](https://github.com/himesamanoyume/HotaruAssistant/releases/latest) 下载

检测更新 双击 `Update.exe`

## 相关项目

HotaruAssistant 离不开以下开源项目的帮助：

- 原版三月七助手 [https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

- 原版模拟宇宙自动化 [https://github.com/CHNZYX/Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe)

- OCR文字识别 [https://github.com/hiroi-sora/PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)

## TODO

- 邮件中没有2.0遗器分解的配置信息
- 遗器判定增加,适应1080P窗口

## 低优先级

- 新增设置开启自动战斗继承和config项
- 当一个事件距离开始不超过1天时 记为新活动开始发送通知
- 补回录制时出现致命错误依旧发送视频附件
- Bug:最后一个账号如果抛出异常进入非正常退出流程,则会直接开始下一轮循环
- Bug:模拟宇宙进行过程中非正常退出时,下次上号仍会处于模拟宇宙中,此时脚本无法识别当前情景（懒得修,自己手动退出模拟宇宙）