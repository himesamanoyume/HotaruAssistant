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

## 声明

- Chinese Support Only
- 随缘更新,没有群(但我在原作者群里),不写Changelog
- 基本不回答问题

**老版本代码已迁移到了old分支**

## 功能对比

功能|原版|此版
--|--|--
**多账号支持**|&cross;|&check;
**遗器胚子识别**|&cross;|&check;(不支持模拟宇宙遗器)
遗器自动分解|&check;|&check;
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
OBS录制|&cross;|&check;(准备取消)

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/himesamanoyume/Auto_Simulated_Universe) 项目也是为我自己适配本项目所修改的fork,非原版模拟宇宙,锄大地功能已经剔除

## 注意事项

- 必须在**PC端**以 `1920*1080` 分辨率运行游戏（不支持HDR）
- 通过使用 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html) 以在后台使用
- 确保已安装Python 3.11.1及以上版本, 调用的模拟宇宙模块为源码运行

> 本项目用于在一个后台用户上完成所有账号的日常周常,若有锄大地等需求建议使用[原版三月七助手](https://github.com/moesnow/March7thAssistant)每个账号开一个用户单独运作,或者直接单独使用原项目仓库中提到的[原版模拟宇宙自动化](https://github.com/CHNZYX/Auto_Simulated_Universe)和[原版锄大地自动化](https://github.com/linruowuyin/Fhoe-Rail)项目

## 下载安装

前往 [Releases](https://github.com/himesamanoyume/HotaruAssistant/releases/latest) 下载

检测更新 双击 `Update.exe`

## 如何使用

1. 启动Server

自动打开webui，查看控制台显示的网页ip地址，记录第二个，你将可以在同一局域网环境内用电脑手机浏览器打开，远程修改配置

2. 若为第一次使用: 启动Register获取注册表

因为支持多账号登录，总不可能傻傻地再输密码，因此需要使用Register登录游戏获取注册表，之后将通过导入注册表完成快速登录。每一个uid对应一个注册表，注册表也以uid命名

3. webui激活uid配置

当获取注册表之后，此时该uid已被列入激活列表，此时你需要到webui的激活界面，填写基础配置信息，进行激活

4. 可选:在首次启动前先在webui的UID总览里修改配置

> 强烈建议开启并配置SMTP服务,收取邮件通知

5. 启动Client

此时应该能看到已激活的uid在列表中，按回车开启循环

---

- 刷侵蚀隧洞时会自动检测遗器词条,满足胚子条件时自动上锁,词条过于垃圾则会自动弃置

5星遗器部位|头部|手部|躯干|脚部|位面球|连结绳
-|-|-|-|-|-|-|
3词条0双暴|弃置|弃置|胚子:双暴主词条|弃置|弃置|弃置
3词条1双暴|胚子|胚子|胚子:双暴,攻击力主词条|胚子:速度/攻击力主词条|胚子:属性伤害加成/攻击力主词条|胚子:非防御力主词条
3词条2双暴|胚子|胚子|胚子|胚子|胚子|胚子
4词条0双暴|弃置|弃置|弃置|弃置|弃置|弃置
4词条1双暴|无视|无视|胚子:双暴主词条|无视|无视|无视
4词条2双暴|胚子|胚子|胚子|胚子|胚子|胚子

## 2.0TODO

- ~~模拟宇宙清理队伍的鼠标点击位置不正确~~
- *如果原本模拟宇宙界面就在第六宇宙，在书本传送至第六时，不会自动开启星球，需要手动点击*(有时出现,有时不出现,不知道怎么复现)
- 战斗识别自动战斗改为跟二倍速同一个方式
- 识别相关改进(抄袭原版)
- - screens.json相关一并优化(抄袭原版)
- 新增小月卡天数检测加进度条
- ~~隔天开始运行时没有做每日清空重新读取~~(待验证)
- 启动游戏时若遇到更新无法处理,重试次数太少跳过太快
- 新增角色死亡处理(目前是尝试1,2,3,4切换角色，如果出现需要复活的界面,则跳转到传送点)
- ~~图片资源更新~~
- 模拟宇宙似乎没有领沉浸奖励
- 也许可以把当前State一起打印
- js混淆(集合作为Build中的一步)
- ~~流程中抛出异常时进行正常退出与非正常退出处理~~
- 每次操作之间间隔太久，需要继续优化[重构完成后]
- 支援角色逻辑需要适配2.0
- 优化:姬子试用流程可缩减[重构完成后]
- - 补充姬子试用专属重开逻辑
- 如果完成了每日,头图显示差异
- 模拟宇宙改造成程序运行
- - 且需要连接到服务器,用于发送日志
- 更换头图至秘密基地
- 教程写明更清晰的使用步骤
- blog和hotaru的重复css样式重新整理为common,hotaru,blog.css
- *dataMgr新增以json存储的每日总情况,单次运行情况*
- 每日检测时间戳时应清除daily_tasks_score,daily_tasks_fin
- BUG: config由于连续加载可能会导致内容丢失
- Build脚本中会显示预计构建版本号,用以检查脚本/资源版本号错漏

### Universe

### Task

### Announcement
- **多线程展示**

### State

### Update

### Socket
- [低优先级]~~Client向Server发送心跳包,同时Server也要进行回应~~,当任何一方长期未接收到心跳包时,判定对方离线并做相应处理,如Client发现Server没了,则直接中止程序

### Screen/Click
- 截图工具加上滚动条

### GameLoop

### Web

#### Web大后期

- 公告和更新检查等模块改为动态页面生成**关系到页面加载速度**
- 实现可输入的input框
- 公告新增带图片显示内容
- - 是否需要内网穿透保护页面
- 新增查看日志页，读取文件夹内日志进行查看，且每次都会对当中的日志做清除颜色代码处理？亦或者做其他用途，看情况
- 尝试实现页面串流游戏画面(类似云游戏)[纯娱乐性质想法,未检验可行性]
- 新增工具页,添加如解锁帧率等功能开关

### Notify

### Config

- 每隔一段时加载一次临时config,先用临时config判断当前时间戳是否为最新,根据此决定是否使用该config以及ReloadConfig

### Data

## v1.xTODO

- 完成每日时截图界面与邮件一并发送防止显示完成了每日但实际上并没有的情况

### v1.x低优先级

- webui显示控制台log
- 新增设置开启自动战斗继承和config项
- 当一个事件距离开始不超过1天时 记为新活动开始发送通知
- 补回录制时出现致命错误依旧发送视频附件
- Bug:最后一个账号如果抛出异常进入非正常退出流程,则会直接开始下一轮循环
- Bug:模拟宇宙进行过程中非正常退出时,下次上号仍会处于模拟宇宙中,此时脚本无法识别当前情景（懒得修,自己手动退出模拟宇宙）