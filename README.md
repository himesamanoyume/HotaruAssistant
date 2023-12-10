<div align="center">
<p>
    <img src="./assets/screenshot/March7th.png">
</p>

<h1>
三月七小助手<br>
March7thAssistant - 私人版

修改者: 姫様の夢
</h1>

原项目地址[https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

</div>

## TODO

- 缺少银枝寒鸦的icon
- workflows里添加common转移到assets中
- client新增检查是否开启server并提示
- ~~flask不在debug时似乎页面的config不会变动~~
- config冲突还未解决(所有config操作前加上config.reload())
- config新增设置多少时间重新开始循环
- workflows的zip重复压缩
- 重新实现检查更新
- ~~flask新增模块化~~
- server关闭时发送给client强制关闭请求
- webui实现注册want_register_accounts **(config save中js新增universe_team相关)**
- webui实现account_active,all_account_active_day
- config save load用队列
- 模拟宇宙脚本中领取沉浸奖励点击的部分可以尝试进行检测
- 新增继续模拟宇宙（继续进度，结束并结算）
- 想办法在screen之间做更快速的联动（优化）

## 功能简介

- **日常**：清体力、每日实训、领奖励、委托、锄大地
- **周常**：历战余响、模拟宇宙、忘却之庭
- 每日实训等任务的完成情况支持消息推送
- 凌晨四点或体力恢复到指定值后自动启动
- 任务完成后声音提示、自动关闭游戏或关机

> 其中模拟宇宙调用的 [Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe) 项目，锄大地调用的 [Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail) 项目

详情见 [配置文件](assets/config/config.example.yaml) 或图形界面设置 

## 注意事项

- 必须使用**PC端** `1920*1080` 分辨率窗口或全屏运行游戏（不支持HDR）
- 需要后台运行或多显示器可以尝试 [远程本地多用户桌面](https://asu.stysqy.top/guide/bs.html)

## 下载安装

前往 [Releases](https://github.com/himesamanoyume/March7thAssistant/releases/latest) 下载

检测更新可以点击图形界面设置最底下的按钮，或双击 `Update.exe`

## 相关项目

March7thAssistantPrivate 离不开以下开源项目的帮助：

- 原版三月七助手 [https://github.com/moesnow/March7thAssistant](https://github.com/moesnow/March7thAssistant)

- 模拟宇宙自动化 [https://github.com/CHNZYX/Auto_Simulated_Universe](https://github.com/CHNZYX/Auto_Simulated_Universe)

- 锄大地自动化 [https://github.com/linruowuyin/Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail)

- OCR文字识别 [https://github.com/hiroi-sora/PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)

- 图形界面组件库 [https://github.com/zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)