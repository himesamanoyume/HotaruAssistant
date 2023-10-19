# Changelog

## v1.6.3

### 新功能
- 支持主动通过“姬子试用”和“回忆一”完成部分每日实训
- Python 3.12.0 强力驱动
- 适配 Fhoe-Rail 的最新改动
### 修复
- “超时时间”修改为小数会导致图形界面启动崩溃
- 无法领取巡光之礼和巡星之礼最后一天的奖励
### 其他
- 优化了现有功能的稳定性
- 现在只会停止当前用户下的游戏进程（实验性）

## v1.6.2

### 新功能
- 支持使用“后备开拓力”和“燃料”
- 支持领取活动“巡光之礼”奖励
- go-cqhttp 支持发送截图 [#21](https://github.com/moesnow/March7thAssistant/pull/21)
### 修复
- 有极小概率将开拓力识别成“米”字
### 其他
- 移除 power_total、dispatch_count、ocr_path 配置项
- 使用消耗品前会先筛选类别避免背包物品太多
- 升级 [PaddleOCR-json_v.1.3.1](https://github.com/hiroi-sora/PaddleOCR-json/releases/tag/v1.3.1)，兼容 Win7 x64
- 支持 [RapidOCR-json_v0.2.0](https://github.com/hiroi-sora/RapidOCR-json/releases/download/v0.2.0/RapidOCR-json_v0.2.0.7z)，兼容没有 AVX2 指令集的 CPU（自动判断）

## v1.6.1

### 新功能
- 预设“副本名称”（包含解释）
- 支持“镜流”和“开拓者（星）•毁灭”
- 支持领取活动“巡星之礼”奖励
- 支持识别“开启无名勋礼”界面
### 修复
- PushPlus推送 [#14](https://github.com/moesnow/March7thAssistant/pull/14)
### 其他
- 支持判断手机壁纸状态
- 支持判断是否购买了“无名客的荣勋”
- 配置队伍改为从手机界面进入而不是按键

## v1.6.0

### 新功能
- 完成混沌回忆后自动领取星琼奖励
- 支持使用集成模式运行锄大地（默认）
- 图形界面新增测试消息推送的功能
- 补全了大部分推送方式所需的配置项（推荐Bark、Server酱、邮箱Smtp）
- 支持从官方启动器获取游戏路径 [#10](https://github.com/moesnow/March7thAssistant/pull/10)
### 修复
- Windows终端高版本提示 “错误 2147942402 (0x80070002)” [#12](https://github.com/moesnow/March7thAssistant/pull/12)
- 低配置电脑检测委托状态偶尔异常
- 优化了 “发生错误: None” 的错误提示
- 开启系统设置 “显示强调色” 导致图形界面显示异常 [#11](https://github.com/moesnow/March7thAssistant/pull/11)
### 其他
- 使用多线程大大缩短了图形界面的加载时间 [#11](https://github.com/moesnow/March7thAssistant/pull/11)
- 优化Python版本检测和依赖安装
- 内置“使用教程”，网页版效果更佳

## v1.5.0

### 新功能
- 优化了“副本名称”、“今日实训”在图形界面的显示方式
- 尝试支持国际服启动界面（简体中文）
- 合并 “退出游戏”、“自动关机” 等功能为 “任务完成后”，默认 “无”
- 循环运行4点启动现在会随机延迟0-10分钟执行
### 修复
- 更新时不会自动关闭图形界面（文件占用导致更新失败）
- 工作目录不正确无法运行（常见于使用任务计划程序）
### 其他
- 自动测速并选择最快的镜像源
- 现在“超时”功能可以正确强制停止“锄大地”、“模拟宇宙”子任务
- 优先使用 Windows Terminal 而不是 conhost
- 弃用 “python_path”、“pip_mirror”、“github_mirror” 等设置项

## v1.4.2

### 新功能
- 内置 [Fhoe-Rail](https://github.com/linruowuyin/Fhoe-Rail) 自动锄大地项目，支持在设置界面单独更新，欢迎给作者点个 Star
- 调整了目录结构，推荐手动进行本次更新，自动更新不会移除不再使用的文件

## v1.4.1.1

### 修复
- 偶尔无法正常领取月卡
- 从环境变量自动获取Python路径失败
- pushplus推送问题（再一次）

## v1.4.1

### 新功能
- 支持忘却之庭和支援角色选择“符玄”和“玲可”
- 增加选项用于开关实训“完成1次「忘却之庭」”（默认关闭）
- 支持任务完成后播放声音提示（默认关闭）
- 支持Windows原生通知（默认开启）
- 优化部分错误提示
### 修复
- 锄大地原版启动报错
- pushplus推送问题

## v1.4.0

### 新功能
- 支持任务完成后自动关机（默认关闭）
- 图形界面导航栏优化
- 图形界面支持深色模式
### 修复
- 延长了点击传送副本后的等待时间

## v1.3.5

### 新功能
- 支持图形界面中修改秘技按键 [#4](https://github.com/moesnow/March7thAssistant/pull/4)
- 支持图形界面中导入配置文件 [#4](https://github.com/moesnow/March7thAssistant/pull/4)
- 支持使用指定好友的支援角色 [#5](https://github.com/moesnow/March7thAssistant/pull/5)
- 下载过程支持显示进度条
### 修复
- 更换手机壁纸，导致委托检测失败

## v1.3.4.2

### 新功能
- 配置文件中新增修改秘技按键 [#3](https://github.com/moesnow/March7thAssistant/pull/3)
### 修复
- 位面分裂活动横幅导致无法自动进入黑塔办公室
- 在图形界面中隐藏“副本所需开拓力”设置项避免误修改
- 尝试解决卡在日常任务“完成1次「忘却之庭」”的问题
- 尝试解决自动战斗未自动开启的问题

## v1.3.4.1

### 修复
- 修改 powershell 命令改用 cmd 运行
- 自动安装 Python 的一些问题，现在可以正常安装（实验性）

## v1.3.4

### 新功能
- 支持忘却之庭和支援角色选择 “丹恒•饮月”
- 支持在设置中打开模拟宇宙和锄大地的原版图形界面（用于设置命途等）
- 支持自动下载安装 Python、PaddleOCR-json （实验性）
- 优化三月七小助手和模拟宇宙的更新功能（实验性）
### 修复
- 非4K分辨率下窗口运行游戏导致功能异常

## v1.3.3.1

### 新功能
- 支持在游戏启动后自动检测并保存游戏路径
- 更新常见问题（FQA）

## v1.3.3

### 新功能
- 支持设置是否领取无名勋礼奖励（默认关闭）
- 添加了更多的错误检测
- 更新常见问题（FQA）

## v1.3.2

### 新功能
- 支持自动开启“自动战斗”
- 支持识别锄大地和模拟宇宙运行状态
- 支持识别游戏更新所导致的需要重启
- 支持在官方启动器打开的情况下启动游戏
- 锄大地和模拟宇宙的脚本遇到错误现在会立即终止
### 修复
- 运行任务后且图形界面未关闭，修改配置会导致时间和日常状态被覆盖
- 启动游戏后未处于主界面判定启动失败（现支持任意已知界面）

## v1.3.1

### 新功能
- 支持模拟宇宙“领取沉浸奖励”，在设置中开启，默认关闭
- 支持单独更新模拟宇宙版本（实验性）
- 图形界面支持自动更新版本（实验性）
- 图形界面支持手动检测更新
- 图形界面增加“更新日志”、“常见问题”等子页面
### 修复
- 优化模拟宇宙完成后的通知截图

## v1.3.0.2

### 新功能
- 恢复 v1.3.0 中移除的使用支援角色（borrow_character_enable）选项
- 副本名称设置为"无"代表即使有对应的实训任务也不会去完成
### 修复
- v1.3.0 混沌回忆星数检测异常

## v1.3.0.1

### 修复
- v1.3.0 通过图形界面生成的配置文件不正确

## v1.3.0

### 新功能
- 支持识别每日实训内容并尝试完成，而不是全部做一遍 [点击查看支持任务](https://github.com/moesnow/March7thAssistant#%E6%AF%8F%E6%97%A5%E5%AE%9E%E8%AE%AD)
- 新增选项每周优先完成三次「历战余响」（默认关闭）
- 副本名称（instance_names）更改为根据副本类型单独设置，同时也会用于“完成1次xxx”的实训任务中
- 移除“使用支援角色”、“强制使用支援角色”、“启用每日拍照”和“启用每日合成/使用 材料/消耗品”配置选项
- 每周模拟宇宙运行前先检查一遍可领取的奖励
### 修复
- 尝试解决低概率下识别副本名称失败
- 彻底解决每日实训是否全部完成检测不可信

## v1.2.6

### 新功能
- 支持更多副本类型：侵蚀隧洞、凝滞虚影、拟造花萼（金）、拟造花萼（赤）
- 设置中的捕获截图功能支持OCR识别文字，可用于复制副本名称

## v1.2.5

### 新功能
- 内置锄大地命令

### 修复
- 开拓力偶尔识别成“1240”而不是“/240”
- 每日实训是否全部完成检测失败

## v1.2.4

### 新功能
- 图形界面支持显示更新日志
- 更新模拟宇宙 [Auto_Simulated_Universe  v5.30](https://github.com/CHNZYX/Auto_Simulated_Universe/tree/f17c5db33a42d7f6e6204cb3e6e83ec2fd208e5e)

### 修复
- 1.3版本的各种UI变化导致的异常

## v1.2.3

### 新功能
- 混沌回忆支持检测每关星数
- 副本名称支持简写，例如【睿治之径】

### 修复
- 偶尔点击速度过快导致领取实训奖励失败
- 鼠标位于屏幕左上角触发安全策略导致点击失效
- 偶尔界面切换速度太慢导致消耗品识别点击位置偏移
- 检测无名勋礼奖励模板图片错误
- 降低部分阈值要求，提高操作成功率
- 移除部分多余的界面检测，提高速度

## v1.2.2

### Features
- feat: add Bailu and Kafka
适配白露和卡芙卡
- feat: forgottenhall support melee character
混沌回忆支持近战角色开怪
- feat: add take_screenshot to gui
图形界面设置中新增捕获截图功能
- feat: add check update to gui
图形界面启动时检测更新
- feat: add tip when start

### Fixes
- fix: use consumables when repeat
消耗品效果未过期导致无法使用
- fix: check_update option not available
更新检测开关不可用
- fix: avoid trailblaze_power overflow
模拟宇宙前后清一次体力避免溢出
- fix: space cause text ocr fail
偶尔会识别出空格导致判断文字失败
- fix: exit function

## v1.2.1

### Features
- feat: auto change team
在打副本和锄大地前可以自动切换队伍
- feat: add submodule Auto_Simulated_Universe
添加模拟宇宙子模块

### Fixes
- fix: switch window problem
游戏窗口偶尔无法切换到前台
- fix: same borrow character
支援角色和原队伍角色相同

## v1.2.0

### Features
- feat: graphical user interface
增加图形用户界面