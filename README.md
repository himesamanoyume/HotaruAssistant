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

- ~~调整先清体力再做每日~~
- ~~Bug: 'NoneType' object is not subscriptable~~
- ~~遗器识别是否有误~~
- 遗器新增设为垃圾,以及分解时对垃圾的选择
- - ~~3词条0暴，4词条0暴为垃圾~~

## 低优先级

- 新增任务堆栈 以每天为单位 每新的一天获取最上层选项为今天的目标 支持插入删除，当列表只剩一个时无限循环。插入删除操作时，1选择要插入的任务2选择对应的位置3决定是插入到前面还是插入到后面
删除时1直接选择对应的任务 删除
- 新增设置开启自动战斗继承和config项
- 当一个事件距离开始不超过1天时 记为新活动开始发送通知
- 支持两个深渊信息查看
- 补回录制时出现致命错误依旧发送视频附件
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

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/himesamanoyume/Auto_Simulated_Universe) 项目(我自己为适配本项目所修改的fork)，锄大地功能已经剔除

## 注意事项

- 必须在**PC端**且通过使用 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html) 在后台以 `1920*1080` 分辨率连接用户并以全屏运行游戏（不支持HDR）

## 下载安装

前往 [Releases](https://github.com/himesamanoyume/himesamanoyume/releases/latest) 下载

检测更新可以点击图形界面设置最底下的按钮，或双击 `Update.exe`

## 相关项目

March7thAssistantPrivate 离不开以下开源项目的帮助：

- 原版三月七助手 [https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

- 原版模拟宇宙自动化 [https://github.com/CHNZYX/Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe)

- OCR文字识别 [https://github.com/hiroi-sora/PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)