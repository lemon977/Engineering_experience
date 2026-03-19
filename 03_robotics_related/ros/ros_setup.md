ROS 一键安装（FishROS）

1. 执行安装脚本
下载并执行 FishROS 安装脚本
wget http://fishros.com/install -O fishros && . fishros

2.运行后按提示选择：
```
 → 安装 ROS1 / ROS2
 → 更换软件源
 → 安装常用工具
```

3. 加载环境，使 ROS 环境变量生效
source ~/.bashrc

4. 验证安装
ROS1版本：roscore
启动核心服务，正常运行说明安装成功
ROS2版本：ros2 topic list
能正常输出话题列表说明安装成功

5. 说明
---
* ROS1 需要手动启动 roscore
* ROS2 无需 roscore，节点自动通信
* 不在 conda 环境中安装 ROS
* 推荐使用系统 Python
---