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

- 模拟宇宙必须指定角色 每次模拟宇宙时检测是否正确选人
- ~~如果有模拟宇宙积分奖励领取 领取后再识别一次积分~~
- *notify时先初始化所有用到的内容再根据情况赋值*(未确定是否需要)
- ~~侵蚀隧洞连续挑战逻辑bug~~
- 加入顶号处理 掉线处理
- 通知邮件加上头图
- 优化:当识别到是实训界面时,都先进行一遍(切换到：时)(再加个logger提示)
- 领取每日活跃度时有些任务名识别不出来 比如**累计触发弱点击破5次**
- 检测到遗器时识别信息词条,加入需求词条,当检测到需求词条时锁上并通知
- 多账号用邮件分别通知
- 新增激活config
```yaml
account_active:
    '100593155':
        isExpired: true # 是否过期,如果过期,启动列表跳过该项
        # if ExpirationDate >= time.time() >= ExpirationDate - 3*86400:
        #   完成上号的邮件当中加入即将过期提醒
        # if time.time() >= ExpirationDate or ActiveDay == 0:
        #   isExpired=true,ActiveDate=0,ActiveDay=0,ExpirationDate=0,
        isWantActive: false # 只有在此项为true时才会重新计算过期时间戳
        # if isWantActive:
        #   if isExpired==true:
        #      ActiveDate=time.time(),isExpired=false
        #   ExpirationDate=ActiveDate+ActiveDay*86400,isWantActive=false
        ActiveDate: 0 # 激活时刻的时间戳
        ActiveDay: 0 # 激活的天数:每次is next day都会减1
        ExpirationDate: 0 # 激活时刻过指定天数的时间戳,代表着过期时刻的时间戳
        BindEmail: '' # 绑定的邮箱

```
- 研究国服国际服切换
- 循环测试完善
- daily_memory_one_team测试是否能写入超出4个角色的候补


