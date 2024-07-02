
<img src="./assets/screenshot/hotaruassistant_banner.png">

<div>

<h1>
    <img src="./assets/static/icon/favicon.ico" align="right">
    HotaruAssistant · 流萤小助手<br>
</h1>

<h6>三月七你别再联系了,我怕流萤误会</h6>

基于March7thAssistant v1.6.2

原项目地址[https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

<p>
    <img alt="" src="https://img.shields.io/github/v/release/himesamanoyume/HotaruAssistant?style=flat-square&logo=github&labelColor=40405f&color=66ccff" />
</p>

</div>

## 声明

- Chinese Support Only
- 本软件分为Server, Client, Updater三个应用程序。其中Server部分**不开源**,介意者勿下载,主要意在防止可能的倒狗行为,本身不会含有恶意代码,放心使用。
- 同时虽然本软件主打多账号支持,但考虑到可能对代练有利,本软件做出限制,**不支持**两个以上账号的使用。本身该软件即为我用于解决枯燥的大号小号每日任务而制作,没理由还给别人方便赚钱。(最主要的是老子拿不到钱)
- 随缘更新,没有群(但我在原作者群里),不写Changelog
- 基本不回答问题

## 功能对比

功能|原版|此版
--|--|--
**遗器胚子筛选**|&cross;|&check;
饰品提取|不知道|&check;
模拟宇宙|&check;|暂时停用
差分宇宙|不知道|还没支持
忘却之庭|&check;|&cross;
虚构叙事|&check;|&cross;
锄大地|&check;|&cross;
消息推送|&check;|仅支持邮件
UI|QT客户端|WebUI

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/himesamanoyume/Auto_Simulated_Universe) 项目也是为我自己适配本项目所修改的fork,非原版模拟宇宙,锄大地功能已经剔除

## 预览

不一定仍是实际画面

###### WEBUI

![web_preview](./assets/screenshot/web_preview.png)

###### SMTP

![smtp_preview](./assets/screenshot/smtp_preview.png)

## 注意事项

- 必须在**PC端**以 `1920*1080` 分辨率运行游戏（不支持HDR）
- 通过使用 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html) 以在后台使用
- 确保已安装Python 3.11.1及以上版本, 调用的模拟宇宙模块为源码运行

> 本项目用于在一个后台用户上完成所有账号的日常周常,若有锄大地等需求建议使用[原版三月七助手](https://github.com/moesnow/March7thAssistant)每个账号开一个用户单独运作,或者直接单独使用原项目仓库中提到的[原版模拟宇宙自动化](https://github.com/CHNZYX/Auto_Simulated_Universe)和[原版锄大地自动化](https://github.com/linruowuyin/Fhoe-Rail)项目

## 遗器筛选

刷侵蚀隧洞时会自动检测遗器属性,满足胚子条件时自动上锁,属性过于垃圾则会自动弃置

亦可在WEBUI中使用**遗器筛选器**添加自定义筛选规则

### 通用全遗器默认筛选规则

5星遗器部位|头部|手部|躯干|脚部|位面球|连结绳
-|-|-|-|-|-|-|
3属性0双暴|弃置|弃置|胚子:双暴主属性|弃置|弃置|弃置
3属性1双暴|胚子|胚子|胚子:双暴,攻击力主属性|胚子:速度/攻击力主属性|胚子:属性伤害提高/攻击力主属性|胚子:非防御力主属性
3属性2双暴|胚子|胚子|胚子|胚子|胚子|胚子
4属性0双暴|弃置|弃置|弃置|弃置|弃置|弃置
4属性1双暴|无视|无视|胚子:双暴主属性|无视|无视|无视
4属性2双暴|胚子|胚子|胚子|胚子|胚子|胚子

---

### BUG
- ?:历战余响次数记录似乎不正常

## TODO

- 差分宇宙适配
- 模拟宇宙重新支持
- 遗器筛选器支持只要求主属性满足条件的情况
- - ~~css颜色优化~~
- [低优先级]长期目标:每日执行速度优化,尽可能最快速最少时间完成一次流程
- [低优先级]新增教程页面

### Socket
- [低优先级]~~Client向Server发送心跳包,同时Server也要进行回应~~,当任何一方长期未接收到心跳包时,判定对方离线并做相应处理,如Client发现Server没了,则直接中止程序

### Screen/Click
- 截图工具加上滚动条

#### Web大后期

- 新增工具页,添加如解锁帧率等功能开关
