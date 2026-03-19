ROS 一键安装（FishROS）

1. 执行安装脚本
wget http://fishros.com/install -O fishros && . fishros
2. 选择安装内容

运行后按提示选择：
1 → 安装 ROS
2 → 更换软件源
3 → 安装常用工具

3. 安装完成后
加载 ROS 环境变量
source ~/.bashrc

4. 验证安装
启动 ROS 核心服务（能正常启动说明安装成功）
roscore

5. 说明
---
 * 推荐在 Ubuntu 使用
 * 不要在 conda 环境中安装 ROS
 * 建议使用系统 Python
---